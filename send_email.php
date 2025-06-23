<?php
// 1. Grab & sanitize inputs
$name    = strip_tags(trim($_POST['name']));
$email   = filter_var(trim($_POST['email']), FILTER_VALIDATE_EMAIL);
$subject = strip_tags(trim($_POST['subject']));

// 2. Build the email
$to      = "jerryjasonchen@gmail.com";
$headers = "From: {$name} <{$email}>\r\n"
         . "Reply-To: {$email}\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";
$body    = "Name/Institution: {$name}\n"
         . "Email: {$email}\n\n"
         . "Subject:\n{$subject}\n";

if (mail($to, "Contact form: “{$subject}”", $body, $headers)) {
  header("Location: thank_you.html");
  exit;
} else {
  echo "Sorry, there was a problem sending your message.";
}
?>