document.addEventListener('DOMContentLoaded', () => {
    // Custom Range Slider sync with value display
    const rangeInputs = document.querySelectorAll('.custom-range');
    rangeInputs.forEach(input => {
        // Optional: Add visual track fill logic here if desired
        input.addEventListener('input', (e) => {
            const val = e.target.value;
            // Can update a visual label if needed
        });
    });

    // Modal Logic
    const openModalBtn = document.getElementById('openModalBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modal = document.getElementById('consentModal');

    if (openModalBtn && modal) {
        openModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            modal.classList.add('active');
        });
    }

    if (closeModalBtn && modal) {
        closeModalBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
    }
});
