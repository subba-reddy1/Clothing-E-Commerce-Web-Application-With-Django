// Dynamic UI Interactions
document.addEventListener('DOMContentLoaded', () => {
    console.log("EmeraldShop JS Initialized");
    
    // Add to Cart Simulation
    const cartBtns = document.querySelectorAll('.add-to-cart-btn');
    cartBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            alert('Item added to secure cloud cart!');
        });
    });
});