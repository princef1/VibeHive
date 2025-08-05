const profiles = [
  {
    image:
      "https://media.istockphoto.com/id/1682296067/photo/happy-studio-portrait-or-professional-man-real-estate-agent-or-asian-businessman-smile-for.jpg?s=612x612&w=0&k=20&c=9zbG2-9fl741fbTWw5fNgcEEe4ll-JegrGlQQ6m54rg=",
    name: "John Doe",
    age: 30,
    distance: "5 km away",
  },
  // Add more profiles here
];

const container = document.getElementById("card-container");

profiles.reverse().forEach((profile) => {
  const card = document.createElement("div");
  card.classList.add("card");

  const img = document.createElement("img");
  img.src = profile.image;
  img.alt = profile.name;

  const br= document.createElement("br");
  const namediv = document.createElement("div");
  namediv.classList.add("name-div");

  const nameparagraph = document.createElement("p");

  const name = document.createElement("span");
  name.textContent = profile.name;
  const age = document.createElement("span");
  age.textContent = profile.age;
  nameparagraph.appendChild(name);
  nameparagraph.appendChild(age);

  const distance = document.createElement("span");
  distance.textContent = profile.distance;

  namediv.appendChild(nameparagraph);
  namediv.appendChild(distance);

  card.appendChild(img);
  card.appendChild(namediv);
  container.appendChild(card);
});
