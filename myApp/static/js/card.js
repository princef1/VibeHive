const profiles = [
  {
    media: [
      {
        type: "image",
        url: "https://media.istockphoto.com/id/1682296067/photo/happy-studio-portrait-or-professional-man-real-estate-agent-or-asian-businessman-smile-for.jpg?s=612x612&w=0&k=20&c=9zbG2-9fl741fbTWw5fNgcEEe4ll-JegrGlQQ6m54rg=",
      },
      {
        type: "image",
        url: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
      },
      {
        type: "video",
        url: "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
      },
      {
        type: "image",
        url: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=800&q=80",
      },
    ],
    name: "John Doe",
    location: "New York",
    tag: ["Art", "Music", "Gaming"],
    age: 30,
  },
  {
    media: [
      {
        type: "image",
        url: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
      },
      {
        type: "image",
        url: "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=800&q=80",
      },
    ],
    name: "Jane Smith",
    location: "New York",
    tag: ["Art", "Music", "Gaming"],
    age: 27,
  },
  {
    media: [
      {
        type: "image",
        url: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=800&q=80",
      },
      {
        type: "image",
        url: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=800&q=80",
      },
    ],
    name: "Carlos Rivera",
    location: "New York",
    tag: ["Art", "Music", "Gaming"],
    age: 32,
  },
];

const container = document.getElementById("card-container");
let swipedProfiles = [];

profiles
  .slice()
  .reverse()
  .forEach((profile) => {
    container.appendChild(createCard(profile));
  });
function createMediaElement(item) {
  if (item.type === "image") {
    const img = document.createElement("img");
    img.src = item.url;
    img.alt = "Profile media";
    return img;
  } else if (item.type === "video") {
    const wrapper = document.createElement("div");
    wrapper.classList.add("video-wrapper");

    const video = document.createElement("video");
    video.src = item.url;
    video.autoplay = true;
    video.muted = false;
    video.loop = false;
    video.playsInline = true;
    video.controls = false; // disable default controls

    // --- Custom controls ---
    const controlsDiv = document.createElement("div");
    controlsDiv.classList.add("custom-controls");

    
    const muteBtn = document.createElement("button");
    muteBtn.textContent = video.muted ? "🔇" : "🔊";
    muteBtn.addEventListener("click", () => {
      e.stopPropagation(); // prevent triggering card navigation
      video.muted = !video.muted;
      muteBtn.textContent = video.muted ? "🔇" : "🔊";
    });

    controlsDiv.appendChild(muteBtn);

    wrapper.appendChild(video);
    wrapper.appendChild(controlsDiv);

    return wrapper;
  }
}

function createCard(profile) {
  const card = document.createElement("div");
  card.classList.add("card");

  if (!profile.media.length || !profile.name || !profile.age) return card;

  const imgDiv = document.createElement("div");
  imgDiv.classList.add("img-div");

  const indicators = document.createElement("div");
  indicators.classList.add("slider-indicators");

  profile.media.forEach((_, i) => {
    const bar = document.createElement("div");
    bar.classList.add("slider-bar");
    if (i === 0) bar.classList.add("active");
    indicators.appendChild(bar);
  });

  let index = 0;
  const mediaEl = createMediaElement(profile.media[index]);
  mediaEl.dataset.index = index;
  imgDiv.appendChild(indicators);
  imgDiv.appendChild(mediaEl);

  imgDiv.addEventListener("click", (e) => {
    const bounds = imgDiv.getBoundingClientRect();
    const clickX = e.clientX - bounds.left;
    const mid = bounds.width / 2;

    index =
      clickX > mid
        ? (index + 1) % profile.media.length
        : (index - 1 + profile.media.length) % profile.media.length;

    imgDiv.innerHTML = "";
    imgDiv.appendChild(indicators);
    const newMedia = createMediaElement(profile.media[index]);
    newMedia.dataset.index = index;
    imgDiv.appendChild(newMedia);

    updateIndicators(indicators, index);
  });

  function updateIndicators(container, activeIndex) {
    container.querySelectorAll(".slider-bar").forEach((bar, i) => {
      bar.classList.toggle("active", i === activeIndex);
    });
  }

  const nameDiv = document.createElement("div");
  nameDiv.classList.add("name-div");

  const nameParagraph = document.createElement("p");
  const name = document.createElement("span");
  name.classList.add("name");
  name.textContent = profile.name;

  const age = document.createElement("span");
  age.classList.add("age");
  age.textContent = `, ${profile.age}`;

  const location = document.createElement("span");
  location.classList.add("location");
  location.textContent = `, ${profile.location}`;

  nameParagraph.appendChild(name);
  nameParagraph.appendChild(location);
  nameParagraph.appendChild(age);

  const tagDiv = document.createElement("div");
  tagDiv.classList.add("tag-div");

  const tagSpans = profile.tag.map((tag) => {
    const span = document.createElement("span");
    span.classList.add("tag");
    span.textContent = tag;
    return span;
  });

  tagSpans.forEach((span, i) => {
    if (i >= 2) span.style.display = "none";
    tagDiv.appendChild(span);
  });

  if (profile.tag.length > 2) {
    const toggleBtn = document.createElement("button");
    toggleBtn.classList.add("ellipsis-btn");
    toggleBtn.textContent = "...";

    let expanded = false;
    toggleBtn.addEventListener("click", () => {
      expanded = !expanded;
      tagSpans.forEach((span, i) => {
        if (i >= 2) span.style.display = expanded ? "inline-block" : "none";
      });
      toggleBtn.textContent = expanded ? "less" : "...";
    });

    tagDiv.appendChild(toggleBtn);
  }

  nameParagraph.appendChild(tagDiv);
  nameDiv.appendChild(nameParagraph);

  card.appendChild(imgDiv);
  card.appendChild(nameDiv);

  return card;
}

function Move(direction) {
  const topCard = container.lastElementChild;
  if (!topCard) return;

  topCard.style.transition = "transform 0.5s ease, opacity 0.5s ease";
  topCard.style.transform =
    direction === "left"
      ? "translateX(-150%) rotate(-20deg)"
      : "translateX(150%) rotate(20deg)";
  topCard.style.opacity = 0;

  setTimeout(() => {
    const index = profiles.length - container.childElementCount;
    swipedProfiles.push({ profile: profiles[index] });
    container.removeChild(topCard);
  }, 500);
}

function undo() {
  if (!swipedProfiles.length) return;
  const last = swipedProfiles.pop();
  container.appendChild(createCard(last.profile));
}

document
  .querySelector(".dislike-button")
  .addEventListener("click", () => Move("left"));
document
  .querySelector(".like-button")
  .addEventListener("click", () => Move("right"));
document.querySelector(".undo-button").addEventListener("click", undo);
