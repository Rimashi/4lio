/* ================================================
   написание отзыва
   ================================================ */

$(function () {
  // MARKDOWN РЕДАКТОР
  const mde = new EasyMDE({
    element: document.getElementById("reviewText"),
    spellChecker: false,
    placeholder: "Поделитесь впечатлениями о книге...",
    toolbar: ["bold", "italic", "|", "quote", "unordered-list", "|", "preview"],
    status: false,
    minHeight: "180px",
  });

  // ЗВЁЗДНЫЙ РЕЙТИНГ
  const labels = {
    5: "5 — Отлично",
    4: "4 — Хорошо",
    3: "3 — Удовлетворительно",
    2: "2 — Неудовлетворительно",
    1: "1 — Плохо",
    0: "0 — Ужасно",
  };

  let selectedRating = null;

  $(".star-rating__star").on("mouseenter", function () {
    const val = +$(this).data("value");
    highlightStars(val);
    $("#starLabel").text(labels[val]);
  });
  $(".star-rating__star")
    .parent()
    .on("mouseleave", function () {
      highlightStars(selectedRating);
      $("#starLabel").text(
        selectedRating ? labels[selectedRating] : "Выберите оценку",
      );
    });
  $(".star-rating__star").on("click", function () {
    selectedRating = +$(this).data("value");
    highlightStars(selectedRating);
    $("#ratingValue").val(selectedRating);
    $("#starLabel").text(labels[selectedRating]);
    $("#ratingError").prop("hidden", true);
  });

  function highlightStars(val) {
    $(".star-rating__star").removeClass("active");
    if (!val) return;
    $(".star-rating__star").each(function () {
      if (+$(this).data("value") <= val) $(this).addClass("active");
    });
  }

  // ВАЛИДАЦИЯ И САБМИТ
  $("#writeReviewForm").on("submit", function (e) {
    e.preventDefault();
    let valid = true;
    $("#reviewFormError").prop("hidden", true);

    if (!selectedRating) {
      $("#ratingError").prop("hidden", false);
      valid = false;
    }
    if (!mde.value().trim()) {
      $("#reviewTextError").prop("hidden", false);
      valid = false;
    }
    if (!valid) {
      $("#reviewFormError").prop("hidden", false);
      return;
    }
    // Если всё ок, отправляем форму
    this.submit();
  });
});
