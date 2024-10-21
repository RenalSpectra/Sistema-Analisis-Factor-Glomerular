// Login

// Add patient

async function AddPatient () {
    let name = document.getElementById('inputName').value;
    let lastName = document.getElementById('inputLastName').value;
    let ci = document.getElementById('inputCI').value;
    let birthdate = document.getElementById('inputDateBirth').value;
    birthdate = birthdate.replace(/-/g, '/');

    const hoy = new Date();
    const nacimiento = new Date(document.getElementById('inputDateBirth').value);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    
    // Si el mes es menor o es el mismo pero el día aún no ha pasado, resta 1 a la edad
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--;
    }

    let age = edad;
    console.log(age);

    let weight = document.getElementById('inputWeight').value;
    let height = document.getElementById('inputHeight').value;
    let radioButton1 = document.getElementById('flexRadioMasculino');
    let radioButton2 = document.getElementById('flexRadioFemenino');

    if (radioButton1.checked) {
        gender = radioButton1.value;
    }
    if (radioButton2.checked) {
        gender = radioButton2.value;
    }
    
    try {
        // Realizar una solicitud POST a la ruta de create_user del backend
        const response = await fetch('http://localhost:5000/patients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ci, name, lastName, birthdate, age, gender, height, weight}),
            credentials: 'include'
        });
        const result = await response.json();
        // Verificar si la solicitud fue exitosa
        if (response.ok) {
            alert('Login successful!');
            window.location.href = result.redirect_url;
        } else {
            alert(`Login failed: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while adding patient. Please try again later.');
    }
}