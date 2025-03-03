js_script = """
    <script>
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'L').classList.add('bbutton-left');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'R').classList.add('bbutton-right');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'U').classList.add('bbutton-up');
    Array.from(window.parent.document.querySelectorAll('button[kind=secondary]')).find(el => el.innerText === 'D').classList.add('bbutton-down');

    const doc = window.parent.document;
    buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
    const left_button = buttons.find(el => el.innerText === 'LEFT');
    const right_button = buttons.find(el => el.innerText === 'RIGHT');
    const up_button = buttons.find(el => el.innerText === 'UP');
    const down_button = buttons.find(el => el.innerText === 'DOWN');

    const left_button2 = buttons.find(el => el.innerText === 'L');
    const right_button2 = buttons.find(el => el.innerText === 'R');
    const up_button2 = buttons.find(el => el.innerText === 'U');
    const down_button2 = buttons.find(el => el.innerText === 'D');


    doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 37: // (37 = left arrow)
            left_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
        case 39: // (39 = right arrow)
            right_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
        case 38: // (39 = right arrow)
            up_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
        case 40: // (39 = right arrow)
            down_button.click();
            window.parent.document.getElementById('player').scrollIntoView();
            break;
    }
    });


    left_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("left")
    });

    right_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("right")
    });

    left_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("left")
    });

    right_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("right")
    });

    up_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("up")
    });

    down_button.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("down")
    });

    up_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("up")
    });

    down_button2.addEventListener("click",function() {
    window.parent.document.getElementById('player').scrollIntoView();
    console.log("down")
    });


    </script>
    """

js_script_optimized = """<script>
const doc = window.parent.document;
const buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));

function addButtonClass(button, className) {
  button.classList.add(className);
}

function scrollPlayerIntoView() {
  doc.getElementById('player').scrollIntoView();
}

const buttonMapping = {
  'L': 'bbutton-left',
  'R': 'bbutton-right',
  'U': 'bbutton-up',
  'D': 'bbutton-down',
  'LEFT': 'left_button',
  'RIGHT': 'right_button',
  'UP': 'up_button',
  'DOWN': 'down_button',
};

const buttonRefs = {};

buttons.forEach((button) => {
  const className = buttonMapping[button.innerText];
  if (className) {
    addButtonClass(button, className);
    buttonRefs[className] = button;
  }
});

doc.addEventListener('keydown', (e) => {
  const keyCodeMapping = {
    37: buttonRefs.left_button,
    38: buttonRefs.up_button,
    39: buttonRefs.right_button,
    40: buttonRefs.down_button,
  };

  const button = keyCodeMapping[e.keyCode];
  if (button) {
    button.click();
    scrollPlayerIntoView();
  }
});

Object.values(buttonRefs).forEach((button) => {
  button.addEventListener('click', () => {
    scrollPlayerIntoView();
    console.log(button.innerText.toLowerCase());
  });
});
</script>"""


js_script_highly_optimized = """<script>
// Execute when DOM is fully loaded for better performance
document.addEventListener('DOMContentLoaded', () => {
  const doc = window.parent.document;
  
  // Cache DOM elements and button references
  const buttonClasses = {
    'L': 'bbutton-left',
    'R': 'bbutton-right',
    'U': 'bbutton-up',
    'D': 'bbutton-down'
  };
  
  const buttonActions = {
    'LEFT': 37,
    'RIGHT': 39,
    'UP': 38,
    'DOWN': 40,
    'L': 37,
    'R': 39,
    'U': 38,
    'D': 40
  };
  
  // Create a mapping of keyCode to button elements for faster lookup
  const keyMap = {};
  const allButtons = doc.querySelectorAll('button[kind=secondary]');
  
  // Process buttons only once
  allButtons.forEach(button => {
    const text = button.innerText;
    
    // Add CSS classes to buttons
    if (buttonClasses[text]) {
      button.classList.add(buttonClasses[text]);
    }
    
    // Create keycode mapping
    if (buttonActions[text]) {
      if (!keyMap[buttonActions[text]]) {
        keyMap[buttonActions[text]] = [];
      }
      keyMap[buttonActions[text]].push(button);
      
      // Add click event listener to scroll player into view
      button.addEventListener('click', () => {
        // Use requestAnimationFrame for smoother scrolling
        requestAnimationFrame(() => {
          const player = doc.getElementById('player');
          if (player) player.scrollIntoView({behavior: 'auto', block: 'center'});
        });
      });
    }
  });
  
  // Debounce function to prevent excessive keydown event handling
  let lastKeyTime = 0;
  doc.addEventListener('keydown', (e) => {
    const now = performance.now();
    if (now - lastKeyTime < 50) return; // 50ms debounce
    lastKeyTime = now;
    
    const buttons = keyMap[e.keyCode];
    if (buttons && buttons.length > 0) {
      buttons[0].click();
      e.preventDefault(); // Prevent default browser scrolling
    }
  });
});
</script>`;"""