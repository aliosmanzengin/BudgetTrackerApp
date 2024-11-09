document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('transaction-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent the default form submission

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        fetch('/transactions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                alert(result.error);
            } else {
                // Append the new transaction to the table body
                const transactionsBody = document.getElementById('transactions-body');
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${result.transaction.id}</td>
                    <td>${result.transaction.date}</td>
                    <td>${result.transaction.amount}</td>
                    <td>${result.transaction.category_id}</td>
                    <td>${result.transaction.notes}</td>
                `;
                transactionsBody.appendChild(newRow);

                alert('Transaction added successfully!');
                form.reset();  // Clear the form after successful submission
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while adding the transaction.');
        });
    });
});
