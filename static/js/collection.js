/* ================================================
   взаимодействие с подборками (страница подборки)
   ================================================ */

$(function () {
  function openModal(id) {
    $(id).addClass("active");
    $("body").addClass("modal-open");
  }
  function closeModal(id) {
    $(id).removeClass("active");
    $("body").removeClass("modal-open");
  }

  $(document).on("click", ".modal__close, .modal__close-btn", function () {
    $(this).closest(".modal__background").removeClass("active");
    $("body").removeClass("modal-open");
  });
  $(document).on("click", ".modal__background", function (e) {
    if (e.target === this) {
      $(this).removeClass("active");
      $("body").removeClass("modal-open");
    }
  });
  $(document).on("keydown", function (e) {
    if (e.key === "Escape") {
      $(".modal__background.active").removeClass("active");
      $("body").removeClass("modal-open");
    }
  });

  // Удалить подборку — форма в модалке
  $("#btnDeleteCollection").on("click", function () {
    const name = $(this).data("collection-name");
    $("#deleteCollectionText").text(
      `Вы уверены? Подборка «${name}» будет удалена. Книги останутся в каталоге.`,
    );
    openModal("#deleteCollectionModal");
  });
  // Форма внутри модалки сама отправляется.

  // Убрать книгу из подборки
  let $cardToRemove = null;
  $(document).on("click", "[data-remove-book]", function () {
    const title = $(this).data("book-title");
    $cardToRemove = $(this).closest(".book-card");
    $("#removeBookText").text(`Убрать книгу «${title}» из подборки?`);
    openModal("#removeBookModal");
  });

  $("#confirmRemoveBook").on("click", function () {
    if ($cardToRemove) {
      // Находим форму удаления внутри карточки и отправляем
      const form = $cardToRemove.find("form[action*='remove']");
      if (form.length) {
        form.submit();
      } else {
        // Если формы нет, просто удаляем карточку (для демо)
        $cardToRemove.fadeOut(250, function () {
          $(this).remove();
          if ($(".book-card").length === 0) {
            $(".catalog__grid").hide();
            $("#collectionEmpty").prop("hidden", false);
          }
        });
      }
      $cardToRemove = null;
    }
    closeModal("#removeBookModal");
  });
});
