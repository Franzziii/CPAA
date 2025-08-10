// disable sang inspect rightclick and any key
document.addEventListener("contextmenu", function (e) {
    e.preventDefault();
});

document.addEventListener("keydown", function (e) {
    if (e.key === "F12" || 
        (e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "J")) || 
        (e.ctrlKey && e.key === "U")) {
        e.preventDefault();
    }
});

// protection dev tools
setInterval(function () {
    let element = new Image();
    Object.defineProperty(element, 'id', {
        get: function () {
            alert("Inspecting is disabled!");
            window.location.href = "about:blank"; 
            throw new Error("DevTools detected!");
        }
    });
    console.log(element);
}, 1000);
// Function sang print
function printReport() {
    var content = document.getElementById('report-section').innerHTML;
    var printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Crime Report</title></head><body>');
    printWindow.document.write(content);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

 document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    togglePassword.addEventListener("click", function () {
    
        const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
        passwordInput.setAttribute("type", type);


        if (type === "text") {
            togglePassword.innerHTML = '<i class="bi bi-eye-slash"></i>';
        } else {
            togglePassword.innerHTML = '<i class="bi bi-eye"></i>';
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    
    flashMessages.forEach(message => {
        // Add fade-out class after 5 seconds
        setTimeout(() => {
            message.classList.add('fade-out');
            
            // Remove element after animation completes
            message.addEventListener('animationend', () => {
                message.remove();
            });
        }, 5000);
    });
});

