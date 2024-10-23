async function AddPatient() {
    let name = document.getElementById('inputName').value;
    let lastname = document.getElementById('inputLastName').value;
    let ci = document.getElementById('inputCI').value;
    let birthdate = document.getElementById('inputDateBirth').value;
    birthdate = birthdate.replace(/-/g, '/');

    const hoy = new Date();
    const nacimiento = new Date(document.getElementById('inputDateBirth').value);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();

    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--;
    }

    let age = edad;
    console.log(age);

    let weight = document.getElementById('inputWeight').value;
    let height = document.getElementById('inputHeight').value;
    let radioButton1 = document.getElementById('flexRadioMasculino');
    let radioButton2 = document.getElementById('flexRadioFemenino');

    let gender;
    if (radioButton1.checked) {
        gender = radioButton1.value;
    }
    if (radioButton2.checked) {
        gender = radioButton2.value;
    }

    try {
        // Realizar una solicitud POST al backend para crear el paciente
        const response = await fetch('http://localhost:5000/patients', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ci, name, lastname, birthdate, age, gender, height, weight }),
            credentials: 'include'
        });

        const result = await response.json();

        // Verificar si la solicitud fue exitosa
        if (response.ok) {
            alert('¡Paciente creado con éxito!');
            // Copiando información
            localStorage.setItem('patientData', JSON.stringify({ name, lastname, ci, birthdate, age, height, weight, gender }));
            // Redirigir a la página del paciente recién creado
            window.location.href = `/patients/${ci}`;
        } else {
            alert(`Error al crear paciente: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al agregar el paciente. Inténtalo nuevamente más tarde.');
    }
}
