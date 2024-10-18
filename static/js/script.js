// LOGIN

document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevenir el envío del formulario por defecto

    // Obtener los valores de los campos de entrada del formulario
    const email = document.getElementById('adminEmail').value;
    const password = document.getElementById('adminPassword').value;

    try {
        // Realizar una solicitud POST a la ruta de login del backend
        const response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include' // Incluir cookies en la solicitud si es necesario
        });

        const result = await response.json();

        // Verificar si la solicitud fue exitosa
        if (response.ok) {
            alert('Login successful!');
            // Redirigir al usuario después del login exitoso
            window.location.href = '/home_admin'; // Cambia esto por la ruta deseada
        } else {
            alert(`Login failed: ${result.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while logging in. Please try again later.');
    }
});