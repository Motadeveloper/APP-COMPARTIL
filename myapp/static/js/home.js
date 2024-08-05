document.addEventListener('DOMContentLoaded', function() {
    const categories = document.querySelectorAll('.category');
    const cards = document.querySelectorAll('.card');

    categories.forEach(category => {
        category.addEventListener('click', function() {
            const categoryId = this.getAttribute('data-category');

            cards.forEach(card => {
                if (categoryId === 'all' || card.getAttribute('data-category') === categoryId) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Simulate click on "All" category to show all cards initially
    document.querySelector('.category[data-category="all"]').click();

    // Intersection Observer API for fade-in effect
    const fadeInElements = document.querySelectorAll('.fade-in');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    fadeInElements.forEach(element => {
        observer.observe(element);
    });
});
