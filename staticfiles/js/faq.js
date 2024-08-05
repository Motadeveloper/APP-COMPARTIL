// faq.js
document.addEventListener("DOMContentLoaded", function () {
    const questionElements = document.querySelectorAll('.question');

    questionElements.forEach((question) => {
        const id = question.getAttribute('data-faq');
        const iconPlus = document.getElementById(`icon-plus-${id}`);
        const iconMinus = document.getElementById(`icon-minus-${id}`);
        const answer = question.nextElementSibling;

        question.addEventListener('click', function () {
            // Fecha todas as respostas antes de abrir a atual
            questionElements.forEach((q) => {
                const qId = q.getAttribute('data-faq');
                const qIconPlus = document.getElementById(`icon-plus-${qId}`);
                const qIconMinus = document.getElementById(`icon-minus-${qId}`);
                const qAnswer = q.nextElementSibling;

                if (qId !== id) {
                    qIconPlus.style.display = 'inline-block';
                    qIconMinus.style.display = 'none';
                    qAnswer.style.display = 'none';
                }
            });

            // Alterna a visibilidade do item atual
            if (iconPlus.style.display !== 'none') {
                iconPlus.style.display = 'none';
                iconMinus.style.display = 'inline-block';
                answer.style.display = 'block';
            } else {
                iconPlus.style.display = 'inline-block';
                iconMinus.style.display = 'none';
                answer.style.display = 'none';
            }
        });

        iconMinus.style.display = 'none';
    });
});
