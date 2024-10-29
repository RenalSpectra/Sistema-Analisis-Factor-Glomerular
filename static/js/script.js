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
        const response = await fetch('/patients', {
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

async function AdminSearchPatient(ci) {
    let patient = ci;
    try {
        // Realizar una solicitud POST al backend para leer el paciente
        const response = await fetch('/admin_search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ patient }),
            credentials: 'include'
        });

        const result = await response.json();

        // Verificar si la solicitud fue exitosa
        if (response.ok) {
            // alert('¡Paciente reconocido con éxito!');
            let patientData = result[0];
            // Copiando información
            let name = patientData.name;
            let lastname = patientData.lastname;
            let ci = patientData.ci;
            let birthdate = (patientData.birthdate).replace(/-/g, '/');
            let age = patientData.age;
            let height = patientData.height;
            let weight = patientData.weight;
            let gender = patientData.gender;

            localStorage.setItem('patientData', JSON.stringify({ name, lastname, ci, birthdate, age, height, weight, gender }));
            // Redirigir a la página del paciente recién creado
            window.location.href = `/patients/${ci}`;
        } else {
            alert(`Error al buscar paciente: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al buscar el paciente. Inténtalo nuevamente más tarde.');
    }
}

async function GoBackInfoPatient() {
    let ci = document.getElementById('m_inputCI').value;
    window.location.href = `/patients/${ci}`;
}

async function ModifyPatient() {
    // let name = document.getElementById('m_inputName').value;
    // let lastname = document.getElementById('m_inputLastName').value;
    let ci = document.getElementById('m_inputCI').value;
    // let birthdate = document.getElementById('m_inputDateBirth').value;
    // birthdate = birthdate.replace(/-/g, '/');

    // const hoy = new Date();
    // const nacimiento = new Date(document.getElementById('m_inputDateBirth').value);
    // let edad = hoy.getFullYear() - nacimiento.getFullYear();
    // const mes = hoy.getMonth() - nacimiento.getMonth();

    // if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
    //     edad--;
    // }

    // let age = edad;

    let weight = document.getElementById('m_inputWeight').value;
    let height = document.getElementById('m_inputHeight').value;
    // let gender = document.getElementById('m_inputGender').value;

    try {
        // Realizar una solicitud POST al backend para leer el paciente
        const response = await fetch(`/patients/${ci}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ height, weight }),
            credentials: 'include'
        });

        const result = await response.json();

        if (response.ok) {
            alert('¡Datos del paciente actualizados con éxito!');
            // Actualizar datos
            let patientData = JSON.parse(localStorage.getItem('patientData'));
            if (patientData) {
                // Actualizar los datos en localStorage
                patientData.height = height;
                patientData.weight = weight;
                localStorage.setItem('patientData', JSON.stringify(patientData));
            } else {
                console.warn('No se encontró patientData en localStorage');
            }
            window.location.href = `/patients/${ci}`;
        } else {
            alert(`Error al actualizar datos de paciente: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al actualizar datos el paciente. Inténtalo nuevamente más tarde.');
    }
}

async function deletePatient() {
    let ci = document.getElementById('floating-inputCI').value;
    console.log('Preevio mensaje confirmacion')
    const confirmation = confirm("¿Estás seguro de que deseas eliminar al paciente? Esta acción no se puede deshacer.");
    console.log('Post mensaje confirmacion')

    if (confirmation) {
        console.log('Mensjae confirmado')

        try {
            const response = await fetch(`/patients/${ci}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include'
            });

            if (response.ok) {
                alert('¡Paciente eliminado con éxito!');
                window.location.href = '/home_admin'; // Ajusta la ruta de redirección según tu aplicación
            } else {
                const result = await response.json();
                alert(`Error al eliminar paciente: ${result.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ocurrió un error al intentar eliminar al paciente. Inténtalo nuevamente más tarde.');
        }
    } else {
        alert('Eliminación cancelada.');
    }
}

async function logOut() {
    try {
        const response = await fetch(`/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        if (response.ok) {
            alert('¡Sesión cerrada!');
            window.location.href = '/'; 
        } else {
            alert(`Error al cerrar sesión: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al intentar cerrar sesión. Inténtalo nuevamente más tarde.');
    }
}

async function searchPatients(){
    try {
        const response = await fetch('/patient_metrics', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });
        
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error.');
    }
}