fetch('../storage/project.json')
    .then(response => response.json())
    .then(data => {
        const cardContainer = document.getElementById('project');
        data.forEach(item => {
            const card = document.createElement('div');
            card.classList.add('card');
            card.innerHTML = `
            <a href="${item.link}" target="_blank" class="project-card">
                <img src="${item.background}" alt="Background" class="card-image" />
                <div class="card-content">
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                </div>
            </a>
      `;
            cardContainer.appendChild(card);
        });
    })
    .catch(error => console.error(error));

document.getElementById('menu-toggle').addEventListener('click', () => {
    const navLinks = document.getElementById('nav-links');
    navLinks.classList.toggle('show');
    const menuIcon = document.getElementById('menu-toggle').querySelector('i');
    if (navLinks.classList.contains('show')) {
        menuIcon.classList.remove('fa-bars');
        menuIcon.classList.add('fa-xmark');
    } else {
        menuIcon.classList.remove('fa-xmark');
        menuIcon.classList.add('fa-bars');
    }
});