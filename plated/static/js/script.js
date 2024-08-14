document.getElementById('toggleBtn').addEventListener('click', function() {
    const sidebar = document.getElementById('side-nav-bar');
    sidebar.classList.toggle('show');
});

document.querySelector('.dropdown-btn').addEventListener('click', function() {
    const dropdownContainer = this.nextElementSibling;
    dropdownContainer.classList.toggle('show');
});
