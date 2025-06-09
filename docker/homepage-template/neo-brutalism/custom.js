// Neo-Brutalism Interactive Effects for Homepage

document.addEventListener('DOMContentLoaded', function() {
  // Effet de typing pour le greeting
  function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    function type() {
      if (i < text.length) {
        element.innerHTML += text.charAt(i);
        i++;
        setTimeout(type, speed);
      }
    }
    type();
  }
  
  // Animation du greeting au chargement
  const greeting = document.querySelector('.information-widget-greeting span');
  if (greeting) {
    const originalText = greeting.textContent;
    setTimeout(() => {
      typeWriter(greeting, originalText, 80);
    }, 1000);
  }
  
  // Effet de shake sur les cartes de service
  function addShakeEffect() {
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.style.animation = 'shake 0.5s ease-in-out';
      });
      
      card.addEventListener('animationend', function() {
        this.style.animation = '';
      });
    });
  }
  
  // Ajout de l'animation shake en CSS
  const shakeStyle = document.createElement('style');
  shakeStyle.textContent = `
    @keyframes shake {
      0%, 100% { transform: rotate(0.5deg) translateX(0); }
      10% { transform: rotate(-0.5deg) translateX(-2px); }
      20% { transform: rotate(0.5deg) translateX(2px); }
      30% { transform: rotate(-0.5deg) translateX(-2px); }
      40% { transform: rotate(0.5deg) translateX(2px); }
      50% { transform: rotate(-0.5deg) translateX(-1px); }
      60% { transform: rotate(0.5deg) translateX(1px); }
      70% { transform: rotate(-0.5deg) translateX(-1px); }
      80% { transform: rotate(0.5deg) translateX(1px); }
      90% { transform: rotate(-0.5deg) translateX(-1px); }
    }
  `;
  document.head.appendChild(shakeStyle);
  
  // Effet de rotation aléatoire pour les icônes
  function randomRotateIcons() {
    const icons = document.querySelectorAll('.service-icon img');
    icons.forEach(icon => {
      const randomRotation = (Math.random() - 0.5) * 6; // Entre -3 et 3 degrés
      icon.style.transform = `rotate(${randomRotation}deg)`;
      
      icon.addEventListener('mouseenter', function() {
        const hoverRotation = (Math.random() - 0.5) * 12; // Rotation plus importante au hover
        this.style.transform = `rotate(${hoverRotation}deg) scale(1.1)`;
      });
      
      icon.addEventListener('mouseleave', function() {
        this.style.transform = `rotate(${randomRotation}deg)`;
      });
    });
  }
  
  // Effet de glitch sur les titres de groupes
  function addGlitchEffect() {
    const groupTitles = document.querySelectorAll('.service-group-name');
    groupTitles.forEach(title => {
      title.addEventListener('click', function() {
        this.style.animation = 'glitch 0.6s ease-in-out';
        setTimeout(() => {
          this.style.animation = '';
        }, 600);
      });
    });
  }
  
  // Effet de parallax léger pour le background
  function addParallaxEffect() {
    let ticking = false;
    
    function updateParallax() {
      const scrolled = window.pageYOffset;
      const parallax = document.body;
      const speed = scrolled * 0.2;
      
      parallax.style.backgroundPosition = `${speed}px ${speed}px`;
      ticking = false;
    }
    
    function requestParallaxTick() {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }
    
    window.addEventListener('scroll', requestParallaxTick);
  }
  
  // Effet de random colors pour les accents
  function randomColorAccents() {
    const colors = ['#00ff41', '#ff6b35', '#32cd32', '#ff1744', '#00bcd4', '#ffc107'];
    const accentElements = document.querySelectorAll('.service-card:hover');
    
    setInterval(() => {
      const randomColor = colors[Math.floor(Math.random() * colors.length)];
      document.documentElement.style.setProperty('--neo-accent', randomColor);
    }, 5000); // Change la couleur d'accent toutes les 5 secondes
  }
  
  // Effet de matrix rain (optionnel, léger)
  function matrixRain() {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0.05';
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    for (let x = 0; x < columns; x++) {
      drops[x] = 1;
    }
    
    function draw() {
      ctx.fillStyle = 'rgba(240, 240, 240, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = '#00ff41';
      ctx.font = fontSize + 'px Courier New';
      
      for (let i = 0; i < drops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length));
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }
    
    setInterval(draw, 100);
  }
  
  // Initialisation de tous les effets
  setTimeout(() => {
    addShakeEffect();
    randomRotateIcons();
    addGlitchEffect();
    addParallaxEffect();
    // matrixRain(); // Décommentez si vous voulez l'effet matrix
  }, 500);
  
  // Easter egg: Konami Code
  let konamiCode = [];
  const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA
  
  document.addEventListener('keydown', function(e) {
    konamiCode.push(e.keyCode);
    
    if (konamiCode.length > konamiSequence.length) {
      konamiCode.shift();
    }
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
      // Activation du mode "ultra neo-brutalism"
      document.body.style.filter = 'hue-rotate(180deg) saturate(2)';
      document.body.style.animation = 'rainbow 2s infinite';
      
      const rainbowStyle = document.createElement('style');
      rainbowStyle.textContent = `
        @keyframes rainbow {
          0% { filter: hue-rotate(0deg) saturate(2); }
          100% { filter: hue-rotate(360deg) saturate(2); }
        }
      `;
      document.head.appendChild(rainbowStyle);
      
      setTimeout(() => {
        document.body.style.filter = '';
        document.body.style.animation = '';
        document.head.removeChild(rainbowStyle);
      }, 10000);
      
      konamiCode = [];
    }
  });
  
  // Notification de mode activé
  const notification = document.createElement('div');
  notification.textContent = '🎨 NEO-BRUTALISM MODE ACTIVATED!';
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #00ff41;
    color: #000;
    padding: 10px 15px;
    border: 3px solid #000;
    box-shadow: 4px 4px 0px 0px #000;
    font-weight: 900;
    font-family: 'Courier New', monospace;
    z-index: 9999;
    animation: slideIn 0.5s ease-out;
  `;
  
  const slideInStyle = document.createElement('style');
  slideInStyle.textContent = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(slideInStyle);
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.5s ease-in forwards';
    const slideOutStyle = document.createElement('style');
    slideOutStyle.textContent = `
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
    `;
    document.head.appendChild(slideOutStyle);
    
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 500);
  }, 3000);
});
