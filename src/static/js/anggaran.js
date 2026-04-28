// anggaran.js
document.addEventListener("DOMContentLoaded", function() {
    // Menu elements
    const menuDetails = document.getElementById('menu-details');
    const menuCatDate = document.getElementById('menu-cat-date');
    
    // View sections
    const viewDetails = document.getElementById('view-details');
    const viewCatDate = document.getElementById('view-cat-date');

    // Switch to Details View
    menuDetails.addEventListener('click', function() {
        if (!viewDetails) return;
        menuDetails.classList.add('active');
        menuCatDate.classList.remove('active');
        
        viewDetails.style.display = 'flex';
        viewCatDate.style.display = 'none';
    });

    // Switch to Category View
    menuCatDate.addEventListener('click', function() {
        if (!viewCatDate) return;
        menuCatDate.classList.add('active');
        menuDetails.classList.remove('active');
        
        viewCatDate.style.display = 'flex';
        viewDetails.style.display = 'none';
    });
    
    // Switch dynamically using Next Button
    const btnNext = document.getElementById('btn-next-view');
    if (btnNext) {
        btnNext.addEventListener('click', function() {
            menuCatDate.classList.add('active');
            menuDetails.classList.remove('active');
            
            viewCatDate.style.display = 'flex';
            viewDetails.style.display = 'none';
        });
    }
    
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

    const form = document.getElementById('anggaran-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const hiddenJumlah = document.getElementById('hidden-jumlah');
            hiddenJumlah.value = amountField.textContent.replace(/[^0-9]/g, '');
        });
    }
});
