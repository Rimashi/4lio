/* ================================================
   Обёртка над Flask API — jQuery ajax
   ================================================ */

const FolioAPI = {
  base: "",

  _req(method, url, data) {
    return $.ajax({
      method,
      url: this.base + url,
      contentType: "application/json",
      data: data ? JSON.stringify(data) : undefined,
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });
  },

  // Книги
  getBooks(params = {}) {
    return this._req("GET", "/books?" + $.param(params));
  },
  getBook(id) {
    return this._req("GET", `/books/${id}`);
  },
  createBook(formData) {
    return $.ajax({
      method: "POST",
      url: this.base + "/books/add",
      data: formData,
      processData: false,
      contentType: false,
    });
  },
  updateBook(id, formData) {
    return $.ajax({
      method: "POST",
      url: this.base + `/books/${id}/edit`,
      data: formData,
      processData: false,
      contentType: false,
    });
  },
  deleteBook(id) {
    return this._req("DELETE", `/books/${id}/delete`);
  },

  // Рецензии
  createReview(bookId, data) {
    return this._req("POST", `/books/${bookId}/reviews/add`, data);
  },
  approveReview(id) {
    return this._req("POST", `/moderation/${id}/approve`);
  },
  rejectReview(id) {
    return this._req("POST", `/moderation/${id}/reject`);
  },

  // Подборки
  getCollections() {
    return this._req("GET", "/collections");
  },
  createCollection(name) {
    return this._req("POST", "/collections/add", { name });
  },
  deleteCollection(id) {
    return this._req("POST", `/collections/${id}/delete`);
  },
  addBookToCollection(collectionId, bookId) {
    return this._req("POST", `/collections/${collectionId}/books/add`, {
      book_id: bookId,
    });
  },
  removeBookFromCollection(collectionId, bookId) {
    return this._req(
      "POST",
      `/collections/${collectionId}/books/${bookId}/remove`,
    );
  },

  // Профиль
  updateProfile(data) {
    return this._req("POST", "/profile/edit", data);
  },
  changePassword(data) {
    return this._req("POST", "/profile/password", data);
  },
  getHistory() {
    return this._req("GET", "/history");
  },
  clearHistory() {
    return this._req("POST", "/history/clear");
  },

  flash(text, type = "info") {
    let $c = $(".flash-messages");
    if (!$c.length)
      $c = $('<div class="flash-messages"></div>').appendTo("body");
    const $f = $(`<div class="flash flash-${type}">${text}</div>`).appendTo($c);
    $f.on("click", () => $f.fadeOut(200, () => $f.remove()));
    setTimeout(() => $f.fadeOut(300, () => $f.remove()), 4000);
  },
};

window.FolioAPI = FolioAPI;
