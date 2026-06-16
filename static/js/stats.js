/* ================================================
   статистика
   ================================================ */

$(function () {
  // ===== ВКЛАДКИ =====
  $(".stats-tab").on("click", function () {
    const tab = $(this).data("tab");
    $(".stats-tab").removeClass("active");
    $(this).addClass("active");
    $(".stats-panel").prop("hidden", true);
    $("#tab" + tab.charAt(0).toUpperCase() + tab.slice(1)).prop(
      "hidden",
      false,
    );
  });

  // ===== CSV ЭКСПОРТ =====
  // Теперь ссылки экспорта ведут на серверные маршруты, поэтому JS только открывает ссылки.
  // Но можно оставить для красоты.
  // Функция downloadCSV больше не нужна, так как сервер отдаёт готовый CSV.
});
