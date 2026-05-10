const form        = document.getElementById("upload-form");
const spinner     = document.getElementById("spinner");
const result      = document.getElementById("result");
const body        = document.getElementById("result-body");
const error       = document.getElementById("error");
const heading     = document.getElementById("main-heading");
const subtitle    = document.getElementById("main-subtitle");
const debugToggle = document.getElementById("debug-toggle");
const debugJson   = document.getElementById("debug-json");

debugToggle.addEventListener("click", () => {
  const expanded = debugToggle.getAttribute("aria-expanded") === "true";
  debugToggle.setAttribute("aria-expanded", !expanded);
  debugToggle.classList.toggle("open", !expanded);
  debugJson.classList.toggle("hidden", expanded);
});

function renderAccommodations(items) {
  if (!items || !items.length) return "";
  const rows = items.map(item => `
    <li class="plan-item">
      <span class="plan-icon">&#10003;</span>
      <div class="plan-content">
        <p class="plan-action">${item.action}</p>
        <p class="plan-ref"><span class="ref-label">IEP</span>${item.iep_reference}</p>
        <p class="plan-ref"><span class="ref-label">Lesson</span>${item.lesson_reference}</p>
      </div>
    </li>`).join("");
  return `
    <section class="result-section">
      <h3>Opportunities for Accommodation</h3>
      <ul class="plan-list">${rows}</ul>
    </section>`;
}

function renderEvaluations(items) {
  if (!items || !items.length) return "";
  const rows = items.map(item => `
    <li class="plan-item">
      <span class="plan-icon eval-icon">&#9744;</span>
      <div class="plan-content">
        <p class="plan-action">${item.observation}</p>
        <p class="plan-ref"><span class="ref-label">IEP Goal</span>${item.iep_goal}</p>
        <p class="plan-ref"><span class="ref-label">Lesson</span>${item.lesson_reference}</p>
      </div>
    </li>`).join("");
  return `
    <section class="result-section">
      <h3>Opportunities for Evaluation</h3>
      <ul class="plan-list">${rows}</ul>
    </section>`;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  error.classList.add("hidden");
  result.classList.add("hidden");
  form.classList.add("hidden");
  spinner.classList.remove("hidden");

  const data = new FormData(form);

  try {
    const response = await fetch("/generate", { method: "POST", body: data });
    const json     = await response.json();

    if (!response.ok) {
      throw new Error(json.error || "Something went wrong.");
    }

    const parsed         = typeof json === "string" ? JSON.parse(json) : json;
    const studentName    = parsed.student_name   || "Unknown Student";
    const lessonDesc     = parsed.lesson         || "";
    const accommodations = parsed.accommodations || [];
    const evaluations    = parsed.evaluations    || [];

    heading.textContent  = `Modified Action Plan: ${studentName}`;
    subtitle.textContent = lessonDesc ? `Lesson: ${lessonDesc}` : "";

    body.innerHTML     = renderAccommodations(accommodations) + renderEvaluations(evaluations);
    debugJson.textContent = JSON.stringify(parsed, null, 2);

    result.classList.remove("hidden");

  } catch (err) {
    form.classList.remove("hidden");
    error.textContent = err.message;
    error.classList.remove("hidden");

  } finally {
    spinner.classList.add("hidden");
  }
});
