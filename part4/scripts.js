// ============================================
// HBnB - Final Clean JavaScript
// ============================================

const API_URL = 'http://127.0.0.1:5000/api/v1';

// ========== Cookie Helpers ==========
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function setCookie(name, value, days = 7) {
    const d = new Date();
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; path=/; expires=${d.toUTCString()}`;
}

function deleteCookie(name) {
    document.cookie = `${name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC`;
}

// ========== Auth Functions ==========
function isAuthenticated() {
    return getCookie('token') !== null;
}

function updateAuthUI() {
    const loginBtn = document.getElementById('login-btn');
    const userMenu = document.getElementById('user-menu');
    const userInitial = document.getElementById('user-initial');
    const email = localStorage.getItem('userEmail');

    if (isAuthenticated() && email) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (userMenu) {
            userMenu.classList.remove('hidden');
            userMenu.classList.add('flex');
        }
        if (userInitial) {
            userInitial.textContent = email.charAt(0).toUpperCase();
        }
    } else {
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (userMenu) {
            userMenu.classList.add('hidden');
            userMenu.classList.remove('flex');
        }
    }
}

function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            deleteCookie('token');
            localStorage.removeItem('userEmail');
            window.location.href = 'index.html';
        });
    }
}

// ========== Login ==========
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            setCookie('token', data.access_token, 7);
            localStorage.setItem('userEmail', email);
            window.location.href = 'index.html';
        } else {
            if (errorMsg) errorMsg.textContent = data.message || 'Invalid credentials';
        }
    } catch (error) {
        if (errorMsg) errorMsg.textContent = 'Connection error';
    }
}

function setupLoginForm() {
    const form = document.getElementById('login-form');
    if (form) {
        form.addEventListener('submit', handleLogin);
    }
}

// ========== Places ==========
async function fetchPlaces() {
    try {
        const response = await fetch(`${API_URL}/places/`);
        if (!response.ok) throw new Error('Failed');
        return await response.json();
    } catch (error) {
        return [];
    }
}

function getPlaceImage(placeId) {
    const images = [
        'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600',
        'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=600',
        'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600',
        'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=600',
        'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=600'
    ];
    const hash = placeId.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return images[hash % images.length];
}

function getAmenitiesIcons(amenities) {
    if (!amenities || amenities.length === 0) return '';
    
    const iconMap = {
        'WiFi': 'fa-wifi',
        'Pool': 'fa-swimming-pool',
        'Parking': 'fa-car',
        'Breakfast': 'fa-coffee',
        'Gym': 'fa-dumbbell',
        'AC': 'fa-snowflake'
    };

    return amenities.slice(0, 4).map(a => {
        const icon = iconMap[a.name] || 'fa-check';
        return `<div class="flex items-center gap-2 text-sm text-gray-600">
            <i class="fas ${icon} text-purple-600"></i>
            <span>${a.name}</span>
        </div>`;
    }).join('');
}

function createPlaceCard(place) {
    const isFavorite = localStorage.getItem(`fav_${place.id}`) === 'true';
    const heartClass = isFavorite ? 'fas' : 'far';

    return `
        <div class="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition relative">
            <button class="absolute top-3 right-3 z-10 w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-md hover:scale-110 transition favorite-btn" data-id="${place.id}">
                <i class="${heartClass} fa-heart text-red-500 text-xl"></i>
            </button>
            
            <img src="${getPlaceImage(place.id)}" class="w-full h-48 object-cover" alt="${place.title}">
            
            <div class="p-4">
                <h3 class="text-xl font-bold mb-2">${place.title}</h3>
                <p class="text-gray-600 text-sm mb-3">${(place.description || '').substring(0, 100)}...</p>
                
                <div class="flex flex-wrap gap-3 mb-4">
                    ${getAmenitiesIcons(place.amenities)}
                </div>
                
                <div class="flex items-center justify-between">
                    <div>
                        <span class="text-2xl font-bold text-purple-600">${place.price_per_night}</span>
                        <span class="text-gray-600 text-sm"> SAR/night</span>
                    </div>
                    <a href="place.html?id=${place.id}" class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold">View</a>
                </div>
            </div>
        </div>
    `;
}

async function displayPlaces() {
    const container = document.getElementById('places-list');
    if (!container) return;
    await displayPlacesInContainer(container, 'price-filter');
}

async function displayPlacesInContainer(container, filterElementId) {
    if (!container) return;

    try {
        const places = await fetchPlaces();
        
        if (!places || places.length === 0) {
            container.innerHTML = '<div class="col-span-full text-center py-12 text-gray-600">No places available</div>';
            return;
        }

        function renderPlaces(list) {
            container.innerHTML = list.map(p => createPlaceCard(p)).join('');
            setupFavorites();
        }

        renderPlaces(places);

        const filter = document.getElementById(filterElementId);
        if (filter) {
            filter.addEventListener('change', (e) => {
                const val = e.target.value;
                if (val === 'all') {
                    renderPlaces(places);
                } else {
                    const filtered = places.filter(p => p.price_per_night <= Number(val));
                    renderPlaces(filtered);
                }
            });
        }
    } catch (error) {
        container.innerHTML = '<div class="col-span-full text-center py-12 text-red-600">Error loading places</div>';
    }
}

function setupFavorites() {
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const id = btn.dataset.id;
            const icon = btn.querySelector('i');
            const isFav = localStorage.getItem(`fav_${id}`) === 'true';

            if (isFav) {
                localStorage.removeItem(`fav_${id}`);
                icon.classList.remove('fas');
                icon.classList.add('far');
            } else {
                localStorage.setItem(`fav_${id}`, 'true');
                icon.classList.remove('far');
                icon.classList.add('fas');
            }
        });
    });
}

// ========== Place Details ==========
async function fetchPlaceDetails(id) {
    try {
        const response = await fetch(`${API_URL}/places/${id}`);
        if (!response.ok) throw new Error('Failed');
        return await response.json();
    } catch (error) {
        return null;
    }
}

async function fetchReviews(placeId) {
    console.log(' Fetching reviews for place:', placeId);
    try {
        const url = `${API_URL}/reviews/?place_id=${placeId}`;
        console.log(' Full URL:', url);
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Response status:', response.status);
        console.log(' Response headers:', response.headers);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(' Response error:', errorText);
            return [];
        }
        
        const data = await response.json();
        console.log(' Reviews data:', data);
        console.log(' Number of reviews:', Array.isArray(data) ? data.length : 'Not an array');
        
        return Array.isArray(data) ? data : [];
    } catch (error) {
        console.error(' Fetch error:', error);
        console.error(' Error type:', error.name);
        console.error(' Error message:', error.message);
        return [];
    }
}

async function displayPlaceDetails() {
    const container = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews-list');
    const addReviewSection = document.getElementById('add-review-section');
    const allPlacesSection = document.getElementById('all-places-section');
    const detailsSection = document.getElementById('place-details-section');
    
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    
    // Show all places if no ID
    if (!id && allPlacesSection) {
        allPlacesSection.classList.remove('hidden');
        if (detailsSection) detailsSection.classList.add('hidden');
        
        const allPlacesList = document.getElementById('all-places-list');
        if (allPlacesList) {
            displayPlacesInContainer(allPlacesList, 'price-filter-places');
        }
        return;
    }
    
    // Show place details if ID exists
    if (!container) return;
    
    if (allPlacesSection) allPlacesSection.classList.add('hidden');
    if (detailsSection) detailsSection.classList.remove('hidden');

    try {
        const place = await fetchPlaceDetails(id);
        
        if (!place) {
            container.innerHTML = '<div class="text-center py-12 text-red-600">Place not found</div>';
            return;
        }

        // Display place details
        container.innerHTML = `
            <div class="bg-white rounded-xl shadow-md overflow-hidden">
                <img src="${getPlaceImage(place.id)}" class="w-full h-96 object-cover" alt="${place.title}">
                <div class="p-6">
                    <h1 class="text-3xl font-bold mb-4">${place.title}</h1>
                    <p class="text-gray-700 mb-4">${place.description || 'No description available'}</p>
                    
                    <div class="flex flex-wrap gap-4 mb-6">
                        ${getAmenitiesIcons(place.amenities)}
                    </div>
                    
                    <div class="text-3xl font-bold text-purple-600">
                        ${place.price_per_night} SAR <span class="text-lg text-gray-600 font-normal">/ night</span>
                    </div>
                </div>
            </div>
        `;

        // Fetch and display reviews
        const reviews = await fetchReviews(id);

        if (reviewsContainer) {
            const reviewsSection = reviewsContainer.closest('#reviews-section');
            if (reviewsSection) {
                const reviewsTitle = reviewsSection.querySelector('h2');
                if (reviewsTitle) {
                    reviewsTitle.textContent = `Reviews (${reviews.length})`;
                }
            }

            if (reviews && reviews.length > 0) {
                reviewsContainer.innerHTML = reviews.map(r => {
                    const userName = r.user?.first_name || 'Anonymous';
                    const userInitial = userName.charAt(0).toUpperCase();
                    const rating = r.rating || 0;
                    const reviewText = r.text || 'No comment';
                    
                    return `
                        <div class="bg-white p-6 rounded-xl shadow-md mb-4 border border-gray-200">
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center gap-3">
                                    <div class="w-12 h-12 bg-gradient-to-br from-purple-600 to-purple-800 rounded-full flex items-center justify-center text-white font-bold text-lg">
                                        ${userInitial}
                                    </div>
                                    <div>
                                        <div class="font-semibold text-gray-900">${userName}</div>
                                        <div class="text-sm text-gray-500">${new Date(r.created_at || Date.now()).toLocaleDateString()}</div>
                                    </div>
                                </div>
                                <div class="flex items-center gap-1 text-yellow-500 text-xl">
                                    ${' '.repeat(rating)}
                                </div>
                            </div>
                            <p class="text-gray-700 leading-relaxed">${reviewText}</p>
                        </div>
                    `;
                }).join('');
            } else {
                reviewsContainer.innerHTML = `
                    <div class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl p-8 text-center">
                        <div class="text-4xl mb-3">💬</div>
                        <p class="text-gray-600 font-semibold mb-2">No reviews yet</p>
                        <p class="text-gray-500 text-sm">Be the first to share your experience!</p>
                    </div>
                `;
            }
        }

        // Setup review form for authenticated users
        if (addReviewSection) {
            if (isAuthenticated()) {
                addReviewSection.classList.remove('hidden');
                
                // Setup star rating and form (order is important!)
                setTimeout(() => {
                    setupReviewForm(id);
                    setupStarRating();
                }, 100);
            } else {
                addReviewSection.innerHTML = `
                    <div class="bg-blue-50 border border-blue-200 rounded-xl p-6 text-center">
                        <p class="text-blue-800 font-semibold mb-3">Want to leave a review?</p>
                        <a href="login.html" class="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold">
                            Sign in to review
                        </a>
                    </div>
                `;
                addReviewSection.classList.remove('hidden');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = '<div class="text-center py-12 text-red-600">Error loading details</div>';
    }
}


// ========== Star Rating ==========
let currentRating = 0;

function setupStarRating() {
    console.log(' Setting up star rating...');
    
    const starContainer = document.getElementById('star-rating');
    const ratingInput = document.getElementById('rating-value');
    
    if (!starContainer || !ratingInput) {
        console.error(' Star elements not found!');
        return;
    }
    
    const stars = starContainer.querySelectorAll('i');
    
    if (!stars.length) {
        console.error(' No star icons found!');
        return;
    }
    
    console.log(' Found', stars.length, 'stars');
    
    // Reset
    currentRating = 0;
    ratingInput.value = 0;
    
    // Add event listeners to each star
    stars.forEach((star, index) => {
        const rating = index + 1;
        
        // Hover effect
        star.addEventListener('mouseenter', () => {
            updateStars(stars, rating);
        });
        
        // Click to select
        star.addEventListener('click', () => {
            currentRating = rating;
            ratingInput.value = rating;
            updateStars(stars, rating);
            console.log(' Rating selected:', rating);
        });
    });
    
    // Reset on mouse leave
    starContainer.addEventListener('mouseleave', () => {
        updateStars(stars, currentRating);
    });
    
    console.log(' Star rating initialized');
}

function updateStars(stars, rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far', 'text-gray-300');
            star.classList.add('fas', 'text-yellow-500');
        } else {
            star.classList.remove('fas', 'text-yellow-500');
            star.classList.add('far', 'text-gray-300');
        }
    });
}

// ========== Review Submission ==========
async function submitReview(placeId, rating, text) {
    const token = getCookie('token');
    
    if (!token) {
        throw new Error('You must be logged in');
    }

    const response = await fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ 
            place_id: placeId, 
            rating: parseInt(rating), 
            text: text 
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to submit');
    }

    return await response.json();
}

function setupReviewForm(placeId) {
    const form = document.getElementById('review-form');
    if (!form) {
        console.warn(' Review form not found');
        return;
    }

    console.log(' Setting up review form for place:', placeId);
    
    // Remove old submit handler if exists
    const oldHandler = form.onsubmit;
    form.onsubmit = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const ratingInput = document.getElementById('rating-value');
        const textInput = document.getElementById('review-text');
        
        if (!ratingInput || !textInput) {
            alert('Form error. Please refresh.');
            return;
        }
        
        const rating = parseInt(ratingInput.value);
        const text = textInput.value.trim();

        console.log(' Submitting - Rating:', rating, 'Text:', text);

        // Validation
        if (!rating || rating === 0) {
            alert(' Please select a rating (click on stars)');
            return;
        }

        if (!text || text.length < 10) {
            alert(' Review must be at least 10 characters');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
        }

        try {
            await submitReview(placeId, rating, text);
            alert(' Review submitted successfully!');
            setTimeout(() => window.location.reload(), 1000);
        } catch (error) {
            console.error(' Error:', error);
            alert(' ' + error.message);
            
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Review';
            }
        }
    });
    
    console.log('Review form ready');
}

// ========== Initialize ==========
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    setupLogout();
    setupLoginForm();
    displayPlaces();
    displayPlaceDetails();
});
