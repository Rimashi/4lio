/* ================================================
   Главная: фильтр, модалка удаления
   ================================================ */

$(function () {
  // ===== МОДАЛКА УДАЛЕНИЯ =====
  const $modal = $("#deleteModal");
  const $modalText = $("#deleteModalText");

  $(document).on("click", "[data-book-title]", function () {
    const title = $(this).data("book-title");
    const id = $(this).data("book-id");
    $modalText.text(`Вы уверены, что хотите удалить книгу «${title}»?`);
    // Устанавливаем action формы удаления
    $("#deleteBookForm").attr("action", `/books/${id}/delete`);
    $modal.addClass("active");
    $("body").addClass("modal-open");
  });

  function closeModal() {
    $modal.removeClass("active");
    $("body").removeClass("modal-open");
  }

  $modal.find(".modal__close, .modal__close-btn").on("click", closeModal);
  $modal.on("click", function (e) {
    if (e.target === this) closeModal();
  });
  $(document).on("keydown", function (e) {
    if (e.key === "Escape" && $modal.hasClass("active")) closeModal();
  });

  // Кнопка "Да, удалить" — submit формы, отдельный обработчик не нужен

  // ===== ФИЛЬТР =====
  let activeFilters = {};

  $("#filterForm").on("submit", function (e) {
    e.preventDefault();
    activeFilters = {
      title: $("#filterTitle").val().trim().toLowerCase(),
      author: $("#filterAuthor").val().trim().toLowerCase(),
      genre: $("#filterGenre").val(),
      year: $("#filterYear").val(),
      pagesFrom: parseInt($("#filterPagesFrom").val()) || null,
      pagesTo: parseInt($("#filterPagesTo").val()) || null,
    };
    applyFilter();
    renderFilterTags();
  });

  function applyFilter() {
    let count = 0;
    $("#booksGrid .book-card").each(function () {
      const $card = $(this);
      const title = $card.data("title").toLowerCase();
      const author = $card.data("author").toLowerCase();
      const genres = String($card.data("genre")).split(" ");
      const year = String($card.data("year"));
      const pages = parseInt($card.data("pages"));

      let show = true;
      if (activeFilters.title && !title.includes(activeFilters.title))
        show = false;
      if (activeFilters.author && !author.includes(activeFilters.author))
        show = false;
      if (
        activeFilters.genre &&
        activeFilters.genre.length &&
        !activeFilters.genre.every((g) => genres.includes(g))
      )
        show = false;
      if (
        activeFilters.year &&
        activeFilters.year.length &&
        !activeFilters.year.includes(year)
      )
        show = false;
      if (activeFilters.pagesFrom && pages < activeFilters.pagesFrom)
        show = false;
      if (activeFilters.pagesTo && pages > activeFilters.pagesTo) show = false;

      $card.toggle(show);
      if (show) count++;
    });

    const hasFilter = Object.values(activeFilters).some(
      (v) => v && (!Array.isArray(v) || v.length),
    );
    if (hasFilter) {
      $("#catalogResults").prop("hidden", false);
      $("#resultsCount").text(
        `Найдено: ${count} ${plural(count, ["книга", "книги", "книг"])}`,
      );
      $("#pagination").toggle(count > 0);
      $("#searchEmpty").prop("hidden", count > 0);
    } else {
      $("#catalogResults").prop("hidden", true);
      $("#pagination").show();
      $("#searchEmpty").prop("hidden", true);
    }
  }

  function renderFilterTags() {
    const $tags = $("#filterTags").empty();
    let hasTags = false;
    if (activeFilters.title) {
      addTag($tags, `Название: ${activeFilters.title}`, "title");
      hasTags = true;
    }
    if (activeFilters.author) {
      addTag($tags, `Автор: ${activeFilters.author}`, "author");
      hasTags = true;
    }
    if (activeFilters.genre && activeFilters.genre.length) {
      const genreName = $("#filterGenre option:selected")
        .map(function () {
          return $(this).text();
        })
        .get()
        .join(", ");
      addTag($tags, `Жанр: ${genreName}`, "genre");
      hasTags = true;
    }
    if (activeFilters.year && activeFilters.year.length) {
      addTag($tags, `Год: ${activeFilters.year.join(", ")}`, "year");
      hasTags = true;
    }
    if (activeFilters.pagesFrom || activeFilters.pagesTo) {
      const from = activeFilters.pagesFrom || "—";
      const to = activeFilters.pagesTo || "—";
      addTag($tags, `Страниц: ${from} – ${to}`, "pages");
      hasTags = true;
    }
    $("#filterTags").prop("hidden", !hasTags);
  }

  function addTag($container, text, key) {
    const $tag = $(`
      <span class="filter-tag">
        ${text}
        <button class="filter-tag__remove" data-key="${key}" title="Убрать фильтр">×</button>
      </span>
    `);
    $container.append($tag);
  }

  $("#filterTags").on("click", ".filter-tag__remove", function () {
    const key = $(this).data("key");
    if (key === "title") {
      $("#filterTitle").val("");
      activeFilters.title = "";
    }
    if (key === "author") {
      $("#filterAuthor").val("");
      activeFilters.author = "";
    }
    if (key === "genre") {
      $("#filterGenre").val([]);
      activeFilters.genre = [];
    }
    if (key === "year") {
      $("#filterYear").val([]);
      activeFilters.year = [];
    }
    if (key === "pages") {
      $("#filterPagesFrom").val("");
      $("#filterPagesTo").val("");
      activeFilters.pagesFrom = null;
      activeFilters.pagesTo = null;
    }
    applyFilter();
    renderFilterTags();
  });

  function resetFilter() {
    $("#filterForm")[0].reset();
    activeFilters = {};
    applyFilter();
    renderFilterTags();
  }

  $("#btnResetFilter, #btnResetFilter2, #btnClearSearch").on(
    "click",
    resetFilter,
  );

  function plural(n, forms) {
    const m = n % 10,
      m100 = n % 100;
    if (m === 1 && m100 !== 11) return forms[0];
    if (m >= 2 && m <= 4 && (m100 < 10 || m100 >= 20)) return forms[1];
    return forms[2];
  }
});
