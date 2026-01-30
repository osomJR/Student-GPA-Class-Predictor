document
  .getElementById("predict-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const resultDiv = document.getElementById("result");
    resultDiv.innerText = "Analyzing your academic performance...";

    const payload = {
      average_attendance_per_course: Number(
        document.getElementById("attendance").value,
      ),
      average_assignments_submission_per_course: Number(
        document.getElementById("assignments").value,
      ),
      average_test_scores_per_course: Number(
        document.getElementById("tests").value,
      ),
      average_class_activities_and_engagements_per_course: Number(
        document.getElementById("engagements").value,
      ),
    };

    try {
      const response = await fetch(
        window.location.hostname === "localhost" ||
          window.location.hostname === "127.0.0.1"
          ? "http://127.0.0.1:5000/predict"
          : "https://predict-mygpa.onrender.com/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        },
      );

      const result = await response.json();

      if (!response.ok) {
        resultDiv.innerText =
          " Error: " + (result.error || "Validation failed");
        return;
      }

      resultDiv.innerText =
        "🎓 Predicted GPA Class:\n" +
        result.prediction +
        "\n\n📌 Personalized Feedback:\n" +
        result.feedback;
    } catch (error) {
      resultDiv.innerText =
        "⚠️ Network or server error. Please try again later.";
    }
  });
