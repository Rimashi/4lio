/* ================================================
   профиль
   ================================================ */

$(function () {
  // Редактировать профиль
  $("#btnEditProfile").on("click", function () {
    $("#profileEditForm").prop("hidden", false);
    $("#profilePasswordForm").prop("hidden", true);
    $("html, body").animate(
      { scrollTop: $("#profileEditForm").offset().top - 100 },
      300,
    );
  });
  $("#btnCancelEdit").on("click", function () {
    $("#profileEditForm").prop("hidden", true);
  });

  // Сменить пароль
  $("#btnChangePassword").on("click", function () {
    $("#profilePasswordForm").prop("hidden", false);
    $("#profileEditForm").prop("hidden", true);
    $("html, body").animate(
      { scrollTop: $("#profilePasswordForm").offset().top - 100 },
      300,
    );
  });
  $("#btnCancelPassword").on("click", function () {
    $("#profilePasswordForm").prop("hidden", true);
  });
});
