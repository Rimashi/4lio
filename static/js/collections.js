/* ================================================
   Подборки: создание, удаление — jQuery
   ================================================ */

$(function () {
  // Открыть модалку "Новая подборка"
  $("#btnNewCollection").on("click", function () {
    $("#newCollectionName").val("");
    $("#newCollectionNameError").prop("hidden", true);
    $("#newCollectionModal").addClass("active");
    $("body").addClass("modal-open");
    setTimeout(() => $("#newCollectionName").focus(), 100);
  });

  // Создать подборку — форма внутри модалки сама отправляется
  // Проверка названия перед отправкой
  $("#btnCreateCollection").on("click", function () {
    const name = $("#newCollectionName").val().trim();
    if (!name) {
      $("#newCollectionNameError").prop("hidden", false);
      return;
    }
    // Если всё ок, отправляем форму (находим её и submit)
    $("#newCollectionForm").submit();
  });

  // Enter в поле названия
  $("#newCollectionName").on("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      $("#btnCreateCollection").trigger("click");
    }
  });

  // Удаление подборки — открываем модалку (форма внутри)
  $(document).on("click", "[data-collection-id]", function () {
    const id = $(this).data("collection-id");
    const name = $(this).data("collection-name");
    $("#deleteCollectionText").text(
      `Вы уверены, что хотите удалить подборку «${name}»? Книги из подборки не будут удалены.`,
    );
    // Устанавливаем action формы удаления
    $("#deleteCollectionForm").attr("action", `/collections/${id}/delete`);
    $("#deleteCollectionModal").addClass("active");
    $("body").addClass("modal-open");
  });

  // Закрытие модалок
  $(document).on("click", ".modal__close, .modal__close-btn", function () {
    closeModal($(this).closest(".modal__background"));
  });
  $(document).on("click", ".modal__background", function (e) {
    if (e.target === this) closeModal($(this));
  });
  $(document).on("keydown", function (e) {
    if (e.key === "Escape") closeModal($(".modal__background.active"));
  });

  function closeModal(selector) {
    $(selector).removeClass("active");
    $("body").removeClass("modal-open");
  }
});
