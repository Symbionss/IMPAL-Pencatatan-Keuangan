// pemasukan.js
document.addEventListener("DOMContentLoaded", function() {
    // Menu elements
    const menuDetails = document.getElementById('menu-details');
    const menuCatDate = document.getElementById('menu-cat-date');
    
    // View sections
    const viewDetails = document.getElementById('view-details');
    const viewCatDate = document.getElementById('view-cat-date');

    // Switch to Details View
    menuDetails.addEventListener('click', function() {
        menuDetails.classList.add('active');
        menuCatDate.classList.remove('active');
        
        viewDetails.style.display = 'flex';
        viewCatDate.style.display = 'none';
    });

    // Switch to Category and Date View
    menuCatDate.addEventListener('click', function() {
        menuCatDate.classList.add('active');
        menuDetails.classList.remove('active');
        
        viewCatDate.style.display = 'flex';
        viewDetails.style.display = 'none';
    });
    
    // Switch to Category and Date View dynamically using Next Button
    const btnNext = document.getElementById('btn-next-view');
    if (btnNext) {
        btnNext.addEventListener('click', function() {
            menuCatDate.classList.add('active');
            menuDetails.classList.remove('active');
            
            viewCatDate.style.display = 'flex';
            viewDetails.style.display = 'none';
        });
    }
    
    // Amount Span logic - Make sure span clears "0" nicely on click
    const amountField = document.getElementById('amount-field');
    
    amountField.addEventListener('focus', function() {
        if(this.textContent.trim() === '0') {
            this.textContent = '';
        }
    });

    amountField.addEventListener('blur', function() {
        if(this.textContent.trim() === '') {
            this.textContent = '0';
        }
    });

    amountField.addEventListener('keypress', function(e) {
        if (!/[0-9]/.test(e.key)) {
            e.preventDefault();
        }
    });

    // Submitting form: sync the contenteditable value to actual hidden input
    const form = document.getElementById('pemasukan-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const hiddenJumlah = document.getElementById('hidden-jumlah');
            hiddenJumlah.value = amountField.textContent.replace(/[^0-9]/g, '');
        });
    }
});
