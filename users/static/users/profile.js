document.addEventListener("DOMContentLoaded", async () => {
  const accessToken = localStorage.getItem("access_token");
  if (!accessToken) {
    window.location.href = "/login/";
    return;
  }

  const urlParts = window.location.pathname.split("/").filter((p) => p !== "");
  const userIdFromUrl = urlParts[urlParts.length - 1];

  const editBtn = document.getElementById("edit-profile-btn");
  const followBtn = document.getElementById("follow-btn");
  const editModal = document.getElementById("edit-modal");

  let nextUserPostsUrl = null;
  let isFetchingUserPosts = false;

  let currentUser = null;
  
  function renderRank(user) {
  const rankContainer = document.getElementById("profile-rank");
  if (!rankContainer) return;

  rankContainer.style.display = "flex";
  rankContainer.style.justifyContent = "center";

  rankContainer.innerHTML = `
    <div style="
      width: 280px;
      border: 1px solid #2a2a35;
      border-radius: 16px;
      padding: 16px 18px;
      box-sizing: border-box;
      margin-bottom:30px;
    ">

      <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
      ">
        <div style="
          font-size: 14px;
          font-weight: 600;
          color: ${user.rank_color || "#7c8cff"};
        ">
          ${user.current_rank || ""}
        </div>

        <div style="
          font-size: 13px;
          color: #8b8b9b;
          font-weight: 500;
          margin-left:110px;
        ">
          ${Math.round(user.rank_score || 0)} REP
        </div>
      </div>

      <div style="
        width: 100%;
        height: 7px;
        background: #111118;
        border-radius: 999px;
        overflow: hidden;
        margin-bottom: 10px;
      ">
        <div style="
          width: ${user.progress || 0}%;
          height: 100%;
          background: ${user.rank_color || "#7c8cff"};
          border-radius: 999px;
        "></div>
      </div>

      <div style="
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: #6f6f80;
      ">
        <span>${user.next_rank || "MAX"}</span>
        <span>${Math.round(user.points_to_next || 0)} REP</span>
      </div>

    </div>
  `;
}

  async function initProfile() {
    try {
      const meRes = await fetch("/api/v1/users/me/", {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      const me = await meRes.json();

      document.getElementById("current-username").textContent = me.username;
      document.getElementById("current-usertag").textContent = `@${me.username}`;
      const currentAvatar = document.getElementById("current-avatar");

      if (me.avatar) {
        currentAvatar.innerHTML = `
          <img
            src="${me.avatar}"
            style="width:100%;height:100%;object-fit:cover;border-radius:50%;"
          >
        `;
      } else {
        currentAvatar.textContent = me.username.charAt(0).toUpperCase();
      }

      document.getElementById("dropdown-profile-link").href =
        `/profile/${me.id}/`;

      const res = await fetch(`/api/v1/users/${userIdFromUrl}/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      const user = await res.json();
      currentUser = user;

      renderRank(user);
      document.getElementById("profile-name").textContent =
        user.first_name || user.username;
      document.getElementById("profile-username").textContent =
      `@${user.username}`;
      
      document.getElementById("profile-job").textContent =
        user.job || "Должность не указана";

      document.getElementById("profile-bio").textContent =
        user.bio || "О себе пока ничего нет...";

      document.getElementById("followers-count").textContent =
        user.followers_count || 0;

      const avatarBig = document.getElementById("profile-avatar-big");
      if (user.avatar) {
        avatarBig.innerHTML = `<img src="${user.avatar}" style="width:100%; height:100%; object-fit:cover;">`;
      } else {
        avatarBig.textContent = user.username.charAt(0).toUpperCase();
      }

      if (String(me.id) === String(user.id)) {
        editBtn.style.display = "block";
      } else {
        followBtn.style.display = "block";

        let isFollowing = user.is_followed || false;

        const updateFollowUI = () => {
          followBtn.textContent = isFollowing ? "Отписаться" : "Подписаться";
          followBtn.style.background = isFollowing ? "transparent" : "#ffffff";
          followBtn.style.color = isFollowing ? "#ffffff" : "#000000";
          followBtn.style.border = isFollowing ? "1px solid #333333" : "none";
        };

        updateFollowUI();

        followBtn.addEventListener("click", async () => {
          try {
            let followRes;

            if (isFollowing) {
              followRes = await fetch(
                `/api/v1/interactions/${userIdFromUrl}/`,
                {
                  method: "DELETE",
                  headers: {
                    Authorization: `Bearer ${accessToken}`,
                    "X-CSRFToken": getCookie("csrftoken"),
                  },
                }
              );
            } else {
              followRes = await fetch(`/api/v1/interactions/`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${accessToken}`,
                  "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ following: userIdFromUrl }),
              });
            }

            if (followRes.ok) {
              isFollowing = !isFollowing;
              updateFollowUI();

              const countEl = document.getElementById("followers-count");
              const current = parseInt(countEl.textContent);
              countEl.textContent = isFollowing ? current + 1 : current - 1;
            }
          } catch (e) {
            console.error("Ошибка при подписке:", e);
          }
        });
      }

      loadUserPosts(user.id);
    } catch (e) {
      console.error("Ошибка загрузки:", e);
    }
  }

  async function loadUserPosts(uid) {
    const container = document.getElementById("user-posts-container");
    const end = document.getElementById("profile-feed-end");

    try {
      const res = await fetch(`/api/v1/posts/user/${uid}/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      const data = await res.json();
      const posts = data.results || data;

      document.getElementById("posts-count").textContent =
        data.count !== undefined ? data.count : posts.length;

      container.innerHTML = "";

      if (posts.length === 0) {
        end.textContent = "Публикаций пока нет.";
        end.style.display = "block";
        return;
      }

      posts.forEach((post) => {
        container.appendChild(createPostElement(post, accessToken));
      });

      nextUserPostsUrl = data.next || null;
      end.style.display = nextUserPostsUrl
        ? "none"
        : "block";
      if (!nextUserPostsUrl) end.textContent = "Все публикации загружены.";

    } catch (e) {
      end.textContent = "Ошибка при загрузке постов.";
      end.style.display = "block";
    }
  }

  async function fetchMoreUserPosts() {
    if (!nextUserPostsUrl || isFetchingUserPosts) return;

    isFetchingUserPosts = true;

    const container = document.getElementById("user-posts-container");
    const end = document.getElementById("profile-feed-end");

    end.textContent = "Загрузка...";
    end.style.display = "block";

    try {
      const res = await fetch(nextUserPostsUrl, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      const data = await res.json();
      const posts = data.results || data;

      posts.forEach((post) => {
        container.appendChild(createPostElement(post, accessToken));
      });

      nextUserPostsUrl = data.next || null;

      end.style.display = nextUserPostsUrl ? "none" : "block";
      if (!nextUserPostsUrl) end.textContent = "Все публикации загружены.";

    } catch (e) {
      console.error("Ошибка при подгрузке постов:", e);
    }

    isFetchingUserPosts = false;
  }

  window.addEventListener("scroll", () => {
    if (
      window.innerHeight + window.scrollY >=
      document.body.offsetHeight - 500
    ) {
      fetchMoreUserPosts();
    }
  });

  if (editBtn) {
    editBtn.addEventListener("click", () => {
      editModal.style.display = "flex";

      document.getElementById("edit-firstname").value =
        document.getElementById("profile-name").textContent;

      document.getElementById("edit-job").value =
        document.getElementById("profile-job").textContent ===
        "Должность не указана"
          ? ""
          : document.getElementById("profile-job").textContent;

      document.getElementById("edit-bio").value =
        document.getElementById("profile-bio").textContent ===
        "О себе пока ничего нет..."
          ? ""
          : document.getElementById("profile-bio").textContent;
    });
  }

  document.getElementById("close-modal")?.addEventListener("click", () => {
    editModal.style.display = "none";
  });

  document.getElementById("edit-profile-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fd = new FormData();
    fd.append("first_name", document.getElementById("edit-firstname").value);
    fd.append("bio", document.getElementById("edit-bio").value);
    fd.append("job", document.getElementById("edit-job").value);

    const avatarFile = document.getElementById("edit-avatar-input").files[0];
    if (avatarFile) fd.append("avatar", avatarFile);

    await fetch(`/api/v1/users/${userIdFromUrl}/`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: fd,
    });

    location.reload();
  });

  await initProfile();

  if (typeof initNotifications === "function")
    initNotifications(accessToken);

  if (typeof initUserMenu === "function")
    initUserMenu();
});