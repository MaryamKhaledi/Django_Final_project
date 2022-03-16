const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const addTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const tbody = document.querySelector(".table-body")
searchField.style.direction = "none";
searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        fetch("/mail_page/searchemail", {
            body: JSON.stringify({'searchText': searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                    console.log('timestamp', timestamp);
                    appTable.style.display = "none";
                    tableOutput.style.display = 'block';
                    if (timestamp.length === 0) {
                        tableOutput.innerHTML = "No results found";

                    } else {
                        data.forEach((item) => {
                            tbody.innerHTML +=
                                `<tr>
                                    <td>${item.receiver}</td>
                                    <td>${item.subject}</td>
                                    <td>${item.body}</td>
                                    <td>${item.timestamp}</td>
                                    </tr>`;
                        });
                    }
                }
            )
        ;
    } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});