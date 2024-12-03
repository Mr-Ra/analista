// app.js
document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("uploadForm");
    const filterForm = document.getElementById("filterForm");
    const fileInput = document.getElementById("fileInput");
    const filePreview = document.getElementById("filePreview");
    const extractionResults = document.getElementById("extractionResults");
    const analysisResults = document.getElementById("analysisResults");
    const eventLogs = document.getElementById("eventLogs");
    const token = localStorage.getItem("accessToken");
    

    const BASE_URL = "http://localhost:8000";

    // File upload and analysis
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            alert("Por favor, selecciona un archivo.");
            return;
        }

        // Limpia el visor y configura la vista previa
        const viewerContainer = document.getElementById("viewerContainer");
        viewerContainer.innerHTML = ""; // Limpia cualquier contenido previo
        const fileType = file.type;

        if (fileType === "application/pdf") {
            // Mostrar el PDF utilizando pdf.js
            const fileURL = URL.createObjectURL(file);
            const loadingTask = pdfjsLib.getDocument(fileURL);
            loadingTask.promise.then(pdf => {
                pdf.getPage(1).then(page => {
                    const scale = 1.5;
                    const viewport = page.getViewport({ scale: scale });

                    const canvas = document.createElement("canvas");
                    const context = canvas.getContext("2d");
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    viewerContainer.appendChild(canvas);
                    page.render({
                        canvasContext: context,
                        viewport: viewport
                    });
                });
            });
            extractionResults.innerHTML = "<span style='color: gray;'>Resolviendo...</span>";
        } else if (fileType.startsWith("image/")) {
            // Mostrar la imagen
            extractionResults.innerHTML = "<span style='color: gray;'>Resolviendo...</span>";
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            viewerContainer.appendChild(img);
        } else {
            viewerContainer.innerHTML = "<p>Formato de archivo no soportado.</p>";
        }

        // Realiza el análisis del archivo
        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(`${BASE_URL}/api/file/analyze`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },                
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Error al analizar el archivo.");
            }

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            extractionResults.innerHTML = `<p style="color: red;">${error.message}</p>`;
        }
    });

    // Historical events filtering
    filterForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const eventType = document.getElementById("typeFilter").value;
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;

        try {
            const response = await fetch(
                `${BASE_URL}/api/events/get_events`,{
                    method: "POST",                    
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"                        
                    },
                    body: JSON.stringify({
                        "event_type":eventType,
                        "start_date":startDate,
                        "end_date":endDate
                    })                                    
            });
            if (!response.ok) {
                throw new Error("Error al obtener el histórico.");
            }

            const events = await response.json();
            displayLogs(events);
        } catch (error) {
            eventLogs.innerHTML = `<p style="color: red;">${error.message}</p>`;
        }
    });

    // Export to Excel
    document.getElementById("exportButton").addEventListener("click", async () => {
        const eventType = document.getElementById("typeFilter").value;
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        try {
            const response = await fetch(`${BASE_URL}/api/events/export_events`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "event_type": eventType,
                    "start_date": startDate,
                    "end_date": endDate
                })
            });
    
            if (response.ok) {
                // Si la respuesta es exitosa, procesar la respuesta como archivo binario
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                // a.download = "event_logs.xlsx"; // Cambia el nombre según corresponda
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            } else {
                console.error("Error al exportar eventos:", response.statusText);
                alert("Hubo un error al generar el reporte.");
            }
        } catch (error) {
            console.error("Error en la solicitud de fetch:", error);
            alert("Hubo un problema con la solicitud.");
        }
    });

    // Helper functions
    function displayResults(result) {
        extractionResults.innerHTML = "<h4>Extracción de Datos:</h4>";

        extractionResults.innerHTML += `
        <pre style="background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto;">
            ${JSON.stringify(result, null, 2)}
        </pre>
    `;
    }

    function displayLogs(events) {
        let tableContent = `<table>
            <tr><th>ID</th><th>Tipo</th><th>Descripción</th><th>Fecha</th></tr>
        `;
        
        events.forEach(event => {
            tableContent += `
                <tr>
                    <td>${event.event_id}</td>
                    <td>${event.event_type}</td>
                    <td>${event.event_description}</td>
                    <td>${event.event_date}</td>
                </tr>
            `;
        eventLogs.innerHTML = tableContent;
        });
        tableContent += `
        </tbody>
    </table>
        `;            
    }
});
