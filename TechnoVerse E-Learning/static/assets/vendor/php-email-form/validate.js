function validateForm() {
  let nameInput = document.getElementById('name');
  let emailInput = document.getElementById('email');
  let subjectInput = document.getElementById('subject');
  let messageInput = document.getElementById('message');
  let isValid = true;

  // Form validation logic
  if (nameInput.value.trim() === '') {
    displayError(nameInput, 'Please enter your name.');
    isValid = false;
  }

  if (emailInput.value.trim() === '') {
    displayError(emailInput, 'Please enter your email.');
    isValid = false;
  } else if (!isValidEmail(emailInput.value.trim())) {
    displayError(emailInput, 'Please enter a valid email.');
    isValid = false;
  }

  if (subjectInput.value.trim() === '') {
    displayError(subjectInput, 'Please enter the subject.');
    isValid = false;
  }

  if (messageInput.value.trim() === '') {
    displayError(messageInput, 'Please enter your message.');
    isValid = false;
  }
  console.log("error")
  return isValid;
}

function displayError(input, errorMessage) {
  let errorContainer = input.nextElementSibling;
  errorContainer.textContent = errorMessage;
  errorContainer.classList.add('error-message');
}

function isValidEmail(email) {
  // Regular expression pattern for email validation
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  return emailPattern.test(email);
}

// Event listener for form submission
let contactForm = document.getElementById('contact-form');
contactForm.addEventListener('submit', function(event) {
  event.preventDefault();

  let isValid = validateForm();

  if (isValid) {
    // Proceed with form submission
    this.submit();
  }
});