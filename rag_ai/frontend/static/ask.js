 
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file");
    const titleInput = document.getElementById("title");
    const urlInput = document.getElementById("urlContent");
    const uploadForm = document.getElementById("uploadForm");
    const alertBox = document.getElementById("alertBox");
  
    function setTitleFromFile() {
      const fileName = fileInput.files[0]?.name;
      if (fileName) {
        titleInput.value = fileName.replace(/\.[^/.]+$/, ""); // Remove file extension
      }
    }
  
    function updateUploadView() {
      const selected = document.getElementById("type").value;
  
      document.getElementById("fileInputSection").classList.toggle("hidden", selected !== "file");
      document.getElementById("textInputSection").classList.toggle("hidden", selected !== "text");
      document.getElementById("urlInputSection").classList.toggle("hidden", selected !== "url");
  
      titleInput.readOnly = true;
  
      if (selected === "text") {
        titleInput.value = "pasted_text_" + new Date().getTime();
      } else if (selected === "url") {
        titleInput.value = urlInput.value || "external_link_" + new Date().getTime();
        titleInput.readOnly = false;
      } else {
        titleInput.value = "";
      }
    }
  
    urlInput.addEventListener("input", (e) => {
      if (document.getElementById("type").value === "url") {
        try {
          const domain = new URL(e.target.value).hostname;
          titleInput.value = domain.replace("www.", "");
        } catch {
          titleInput.value = "external_link_" + new Date().getTime();
        }
      }
    });
  
    uploadForm.addEventListener("submit", (event) => {
      event.preventDefault();
  
      const type = document.getElementById("type").value;
      const formData = new FormData();
      formData.append("title", titleInput.value);
  
      if (type === "file") {
        if (fileInput.files.length > 0) {
          formData.append("file", fileInput.files[0]);
        }
        formData.append("content", "");
      } else if (type === "text") {
        formData.append("content", document.getElementById("content").value);
      } else if (type === "url") {
        formData.append("content", urlInput.value);
      }
  
      fetch("/ingest", {
        method: "POST",
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          alertBox.style.display = "block";
          alertBox.textContent = "Uploaded to database successfully";
          alertBox.className = "alert success";
        })
        .catch((error) => {
          alertBox.style.display = "block";
          alertBox.textContent = "Upload failed. Please try again.";
          alertBox.className = "alert error";
          console.error("Upload Error:", error);
        });
    });
  
    fileInput.addEventListener("change", setTitleFromFile);
    document.getElementById("type").addEventListener("change", updateUploadView);
    window.onload = updateUploadView;
  });
  