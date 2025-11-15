/**
 * Admin Panel Asynchronous Filtering
 * Handles AJAX-based filtering for admin list pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fraud Detection Filter Handler
    const fraudFilterButtons = document.querySelectorAll('[data-fraud-filter]');
    if (fraudFilterButtons.length > 0) {
        initFraudDetectionFilters();
    }

    // Investment Products Filter Handler
    const investmentFilterForm = document.getElementById('investmentFilterForm');
    if (investmentFilterForm) {
        initInvestmentProductFilters();
    }
});

/**
 * Initialize Fraud Detection Filters
 */
function initFraudDetectionFilters() {
    const filterButtons = document.querySelectorAll('[data-fraud-filter]');
    const tableContainer = document.getElementById('fraudTableContainer');

    if (!tableContainer) {
        console.warn('Fraud table container not found');
        return;
    }

    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const filterType = this.getAttribute('data-fraud-filter');
            const filterValue = this.getAttribute('data-fraud-value');

            // Update active state
            document.querySelectorAll(`[data-fraud-filter="${filterType}"]`).forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');

            // Make AJAX request
            fetchFraudData(filterType, filterValue);
        });
    });
}

/**
 * Fetch Fraud Data via AJAX
 */
function fetchFraudData(filterType, filterValue) {
    const params = new URLSearchParams();

    if (filterValue) {
        params.append(filterType, filterValue);
    }

    // Get current filters to combine them
    const currentStatus = document.querySelector('[data-fraud-filter="status"].active')?.getAttribute('data-fraud-value');
    const currentRisk = document.querySelector('[data-fraud-filter="risk"].active')?.getAttribute('data-fraud-value');

    if (currentStatus) params.set('status', currentStatus);
    if (currentRisk) params.set('risk', currentRisk);

    const url = new URL(window.location);
    url.search = params.toString();

    // Show loading state
    const tableContainer = document.getElementById('fraudTableContainer');
    const originalContent = tableContainer.innerHTML;
    tableContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    fetch(window.location.pathname + '?ajax=true&' + params.toString(), {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.text();
    })
    .then(html => {
        tableContainer.innerHTML = html;

        // Update URL without page reload
        window.history.pushState({}, '', url);
    })
    .catch(error => {
        console.error('Error fetching fraud data:', error);
        tableContainer.innerHTML = originalContent;
        alert('Error loading filtered data. Please try again.');
    });
}

/**
 * Initialize Investment Product Filters
 */
function initInvestmentProductFilters() {
    const form = document.getElementById('investmentFilterForm');
    const platformSelect = document.getElementById('platformFilter');
    const submitBtn = document.getElementById('investmentFilterSubmit');
    const resetBtn = document.getElementById('investmentFilterReset');

    if (!platformSelect) return;

    // Handle filter submission via AJAX
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        fetchInvestmentProducts();
    });

    // Handle reset
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            platformSelect.value = '';
            fetchInvestmentProducts();
        });
    }

    // Optional: Submit on change for better UX
    platformSelect.addEventListener('change', function() {
        fetchInvestmentProducts();
    });
}

/**
 * Fetch Investment Products via AJAX
 */
function fetchInvestmentProducts() {
    const platformId = document.getElementById('platformFilter').value;
    const params = new URLSearchParams();

    if (platformId) {
        params.append('platform', platformId);
    }

    const url = new URL(window.location);
    url.search = params.toString();

    // Show loading state
    const tableContainer = document.getElementById('investmentTableContainer');
    if (!tableContainer) return;

    const originalContent = tableContainer.innerHTML;
    tableContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';

    fetch(window.location.pathname + '?ajax=true&' + params.toString(), {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.text();
    })
    .then(html => {
        tableContainer.innerHTML = html;

        // Update URL without page reload
        window.history.pushState({}, '', url);
    })
    .catch(error => {
        console.error('Error fetching investment products:', error);
        tableContainer.innerHTML = originalContent;
        alert('Error loading filtered data. Please try again.');
    });
}
