/* ================================================
   Форма книги: мультиселект, превью обложки,
   Markdown-редактор, валидация — jQuery
   ================================================ */

$(function () {
  // Определяем режим: редактирование, если есть поле book_id
  const isEdit = $("#bookId").length > 0;

  if (isEdit) {
    $("#coverUploadBlock").hide();
    $("#coverCurrentBlock").show();
  } else {
    $("#coverUploadBlock").show();
    $("#coverCurrentBlock").hide();
  }

  // MARKDOWN РЕДАКТОР (EasyMDE)
  const mde = new EasyMDE({
    element: document.getElementById("bookDescription"),
    spellChecker: false,
    autofocus: false,
    placeholder:
      "Опишите книгу. Поддерживается **жирный**, *курсив*, > цитаты и т.д.",
    toolbar: [
      "bold",
      "italic",
      "strikethrough",
      "|",
      "heading-2",
      "heading-3",
      "|",
      "quote",
      "unordered-list",
      "ordered-list",
      "|",
      "link",
      "|",
      "preview",
      "side-by-side",
      "fullscreen",
      "|",
      "guide",
    ],
    status: false,
    minHeight: "200px",
  });

  // МУЛЬТИСЕЛЕКТ ЖАНРОВ
  const $selected = $("#genreSelected");
  const $input = $("#genreSearch");
  const $dropdown = $("#genreDropdown");
  const $hiddenSelect = $("#bookGenres");

  $input.on("focus click", function () {
    $dropdown.prop("hidden", false);
    filterOptions("");
  });

  $input.on("input", function () {
    filterOptions($(this).val().toLowerCase());
    $dropdown.prop("hidden", false);
  });

  $(document).on("click", function (e) {
    if (!$(e.target).closest("#genreMultiselect").length) {
      $dropdown.prop("hidden", true);
      $input.val("");
      filterOptions("");
    }
  });

  $dropdown.on("click", ".multiselect__option", function () {
    const val = $(this).data("value");
    const text = $(this).text().trim();
    if ($(this).hasClass("selected")) {
      removeGenre(val);
    } else {
      addGenre(val, text);
    }
    $input.val("").focus();
    filterOptions("");
  });

  $selected.on("click", ".multiselect__tag-remove", function (e) {
    e.stopPropagation();
    const val = $(this).data("value");
    removeGenre(val);
  });

  function addGenre(val, text) {
    const $tag = $(`
      <span class="multiselect__tag">
        ${text}
        <button type="button" class="multiselect__tag-remove" data-value="${val}">×</button>
      </span>
    `);
    $input.before($tag);
    $hiddenSelect.find(`option[value="${val}"]`).prop("selected", true);
    $dropdown
      .find(`.multiselect__option[data-value="${val}"]`)
      .addClass("selected");
  }

  function removeGenre(val) {
    $selected
      .find(`.multiselect__tag-remove[data-value="${val}"]`)
      .closest(".multiselect__tag")
      .remove();
    $hiddenSelect.find(`option[value="${val}"]`).prop("selected", false);
    $dropdown
      .find(`.multiselect__option[data-value="${val}"]`)
      .removeClass("selected");
  }

  function filterOptions(query) {
    $dropdown.find(".multiselect__option").each(function () {
      const text = $(this).text().toLowerCase();
      $(this).toggleClass("hidden", query.length > 0 && !text.includes(query));
    });
  }

  // Инициализация: пометить выбранные
  $hiddenSelect.find("option:selected").each(function () {
    $dropdown
      .find(`.multiselect__option[data-value="${$(this).val()}"]`)
      .addClass("selected");
  });

  // ПРЕВЬЮ ОБЛОЖКИ
  $("#coverUploadBtn").on("click", function () {
    $("#coverFile").trigger("click");
  });

  $("#coverFile").on("change", function () {
    const file = this.files[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      $("#coverError")
        .text("Файл слишком большой. Максимум 5 МБ")
        .prop("hidden", false);
      return;
    }
    if (!file.type.startsWith("image/")) {
      $("#coverError")
        .text("Допустимы только изображения (JPG, PNG, WebP)")
        .prop("hidden", false);
      return;
    }
    $("#coverError").prop("hidden", true);
    const reader = new FileReader();
    reader.onload = function (e) {
      $("#coverPlaceholder").hide();
      $("#coverImg").attr("src", e.target.result).prop("hidden", false);
    };
    reader.readAsDataURL(file);
    $("#coverUploadBtn").html(`
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
      ${file.name}
    `);
  });

  $("#coverPreview")
    .on("dragover", function (e) {
      e.preventDefault();
      $(this).addClass("cover-preview--drag");
    })
    .on("dragleave drop", function (e) {
      e.preventDefault();
      $(this).removeClass("cover-preview--drag");
      if (e.type === "drop") {
        const file = e.originalEvent.dataTransfer.files[0];
        if (file) {
          const dt = new DataTransfer();
          dt.items.add(file);
          $("#coverFile")[0].files = dt.files;
          $("#coverFile").trigger("change");
        }
      }
    });

  // ВАЛИДАЦИЯ И САБМИТ
  $("#bookForm").on("submit", function (e) {
    e.preventDefault();
    let valid = true;
    $(".form-error").prop("hidden", true);
    $(".form-control").removeClass("form-control--error");
    $("#formError").prop("hidden", true);

    if (!$("#bookTitle").val().trim()) {
      showFieldError("bookTitle", "bookTitleError");
      valid = false;
    }
    if (!$("#bookAuthor").val().trim()) {
      showFieldError("bookAuthor", "bookAuthorError");
      valid = false;
    }
    const year = parseInt($("#bookYear").val());
    if (!year || year < 1000 || year > 2099) {
      showFieldError("bookYear", "bookYearError");
      valid = false;
    }
    const pages = parseInt($("#bookPages").val());
    if (!pages || pages < 1) {
      showFieldError("bookPages", "bookPagesError");
      valid = false;
    }
    if (!$("#bookPublisher").val().trim()) {
      showFieldError("bookPublisher", "bookPublisherError");
      valid = false;
    }
    if ($hiddenSelect.find("option:selected").length === 0) {
      $("#bookGenresError").prop("hidden", false);
      $("#genreMultiselect .multiselect__selected").css(
        "border-color",
        "var(--danger-text)",
      );
      valid = false;
    }
    if (!mde.value().trim()) {
      $("#bookDescriptionError").prop("hidden", false);
      $(".EasyMDEContainer .CodeMirror").css(
        "border-color",
        "var(--danger-text)",
      );
      valid = false;
    }
    if (!isEdit && !$("#coverFile")[0].files.length) {
      $("#coverError").text("Загрузите обложку книги").prop("hidden", false);
      valid = false;
    }

    if (!valid) {
      $("#formError").prop("hidden", false);
      const $firstError = $(".form-error:visible").first();
      if ($firstError.length) {
        $("html, body").animate(
          { scrollTop: $firstError.offset().top - 100 },
          300,
        );
      }
      return;
    }

    // Если всё ок, отправляем форму
    this.submit();
  });

  function showFieldError(fieldId, errorId) {
    $("#" + fieldId).addClass("form-control--error");
    $("#" + errorId).prop("hidden", false);
  }

  // Снимаем ошибку при вводе
  $(document).on("input change", ".form-control", function () {
    $(this).removeClass("form-control--error");
    $(this).siblings(".form-error").prop("hidden", true);
    $("#genreMultiselect .multiselect__selected").css("border-color", "");
    $("#bookGenresError").prop("hidden", true);
    $(".EasyMDEContainer .CodeMirror").css("border-color", "");
    $("#bookDescriptionError").prop("hidden", true);
  });
});
