function togglePassword(icon) {
    const input = icon.previousElementSibling;
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // For signup page toggle password icon visibility
    const passwordFields = document.querySelectorAll('.password-container input[type="password"]');
    passwordFields.forEach(function (input) {
        const icon = input.parentElement.querySelector('.toggle-password');

        function updateVisibility() {
            if (input.value.trim() !== '') {
                icon.style.display = 'block';
            } else {
                icon.style.display = 'none';
                input.type = 'password';
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
            }
        }

        input.addEventListener('input', updateVisibility);
        updateVisibility();
    });

    // For login page toggle password icon visibility
    const passwordInput = document.querySelector('input[type="password"], input[name="password"]');
    const toggleIcon = document.querySelector('.toggle-password');

    if (passwordInput && toggleIcon) {
        function updateToggleVisibility() {
            if (passwordInput.value.trim() !== '') {
                toggleIcon.style.display = 'block';
            } else {
                toggleIcon.style.display = 'none';
                passwordInput.type = 'password';
                toggleIcon.classList.remove("fa-eye-slash");
                toggleIcon.classList.add("fa-eye");
            }
        }

        passwordInput.addEventListener('input', updateToggleVisibility);
        updateToggleVisibility();
    }

    // Disable first empty option in birthdate selects
    document.querySelectorAll('.birthdate-boxes select').forEach(function (select) {
        const firstOption = select.options[0];
        if (firstOption && firstOption.value === "") {
            firstOption.disabled = true;
        }
    });
});
