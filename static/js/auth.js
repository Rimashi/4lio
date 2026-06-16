/* ================================================
   Логин / регистрация — jQuery
   ================================================ */

$(function () {
  // Табы
  $(".auth-tab").on("click", function () {
    const tab = $(this).data("tab");
    $(".auth-tab").removeClass("active");
    $(this).addClass("active");
    if (tab === "login") {
      $("#loginForm").prop("hidden", false);
      $("#registerForm").prop("hidden", true);
    } else {
      $("#loginForm").prop("hidden", true);
      $("#registerForm").prop("hidden", false);
    }
    $("#authError").prop("hidden", true);
  });

  // Показать/скрыть пароль
  $(document).on("click", ".input-password__toggle", function () {
    const $input = $(this).siblings(".form-control");
    const $eyeShow = $(this).find(".eye-show");
    const $eyeHide = $(this).find(".eye-hide");
    if ($input.attr("type") === "password") {
      $input.attr("type", "text");
      $eyeShow.hide();
      $eyeHide.show();
    } else {
      $input.attr("type", "password");
      $eyeShow.show();
      $eyeHide.hide();
    }
  });

  // Валидация совпадения паролей
  $("#regPasswordConfirm").on("input", function () {
    const pass = $("#regPassword").val();
    const confirm = $(this).val();
    if (confirm.length > 0 && pass !== confirm) {
      $("#passwordMismatch").prop("hidden", false);
      $(this).addClass("form-control--error");
    } else {
      $("#passwordMismatch").prop("hidden", true);
      $(this).removeClass("form-control--error");
    }
  });

  // Клиентская валидация перед отправкой — не блокируем отправку,
  // а показываем ошибки и, если всё ок, форма отправится сама.
  // Но мы можем добавить проверки на пустые поля.
  // Поскольку форма имеет action, мы позволим браузеру отправлять.
  // Однако для красоты можно добавить проверку и предотвратить отправку,
  // если есть ошибки, но это уже по желанию.
  // Оставим пока как есть, так как сервер тоже валидирует.
});
