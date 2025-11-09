/**
 * Matrix Rain Effect - Neon Digital Rainfall Background
 * Creates a dynamic Matrix-style falling characters animation
 */

class MatrixRain {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.fontSize = 16;
        this.columns = 0;
        this.drops = [];
        this.animationId = null;
        this.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()_+-=[]{}|;:,.<>?/~`";
    }

    init() {
        // Create canvas element
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'matrix-rain';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.zIndex = '-1';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.opacity = '0.15';
        
        document.body.insertBefore(this.canvas, document.body.firstChild);
        
        this.ctx = this.canvas.getContext('2d');
        this.resize();
        
        // Handle window resize
        window.addEventListener('resize', () => this.resize());
        
        // Start animation
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.columns = Math.floor(this.canvas.width / this.fontSize);
        
        // Initialize drops array
        this.drops = [];
        for (let i = 0; i < this.columns; i++) {
            this.drops[i] = Math.floor(Math.random() * this.canvas.height / this.fontSize);
        }
    }

    draw() {
        // Semi-transparent black background for trail effect
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Set text style with neon green color
        this.ctx.fillStyle = '#0F0';
        this.ctx.font = `${this.fontSize}px monospace`;
        
        // Draw characters
        for (let i = 0; i < this.drops.length; i++) {
            // Random character from the character set
            const char = this.characters[Math.floor(Math.random() * this.characters.length)];
            const x = i * this.fontSize;
            const y = this.drops[i] * this.fontSize;
            
            // Draw the character
            this.ctx.fillText(char, x, y);
            
            // Reset drop to top randomly or move it down
            if (y > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
            
            // Move drop down
            this.drops[i]++;
        }
    }

    animate() {
        this.draw();
        this.animationId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
    }
}

// Initialize Matrix Rain on page load
document.addEventListener('DOMContentLoaded', () => {
    const matrixRain = new MatrixRain();
    matrixRain.init();
});
