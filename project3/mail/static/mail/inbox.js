document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-error').innerHTML = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
    .then(r => r.json()
      .then(emails => emails.forEach(email => {
        const sender = document.createElement('p')
        sender.innerHTML = email.sender;
        sender.className = 'font-weight-bold d-inline mr-2 ml-2';
        const subject = document.createElement('p');
        subject.innerHTML = email.subject;
        subject.className = 'd-inline ml-2';
        const timestamp = document.createElement('p');
        timestamp.innerHTML = email.timestamp;
        timestamp.className = 'float-right d-inline mb-0 mr-2';
        const read = email.read;

        const div = document.createElement('div');
        div.appendChild(sender);
        div.appendChild(subject);
        div.appendChild(timestamp);
        div.className = 'border border-dark rounded mb-2 email';
        if (read) {
          div.classList.add('read');
        }
        div.addEventListener('click', () => load_email(email.id));
        document.querySelector('#emails-view').appendChild(div);
    })))
}

function send_email() {
  document.getElementById('#compose-error').innerHTML = '';

  const recipients = document.querySelector('#compose-recipients');
  const subject = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body')

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients.value,
      subject: subject.value,
      body: body.value
    })
  })
    .then(r => r.json().then(data => {
      if (r.status === 201) {
        recipients.value = '';
        subject.value = '';
        body.value = '';
        load_mailbox('sent');
      } else if (r.status === 400) {
        const error = document.querySelector('#compose-error')
        error.innerHTML = data.error;
      }
    }));
  
  return false;
}

function load_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch('/emails/' + id)
    .then(r => r.json().then(data => {
      document.querySelector('#email-sender').innerHTML = data.sender;
      document.querySelector('#email-recipients').innerHTML = data.recipients;
      document.querySelector('#email-title').innerHTML =  data.subject;
      document.querySelector('#email-body').innerHTML = data.body;
      document.querySelector('#email-timestamp').innerHTML = data.timestamp;

      fetch('/emails/' + data.id, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }))
}

function error_alert(msg) {
  div = document.createElement('div');
  div.className = 'alert alert-danger';
  div.style.position = 'fixed';
  div.innerHTML = msg;
  document.appendChild(div);
}