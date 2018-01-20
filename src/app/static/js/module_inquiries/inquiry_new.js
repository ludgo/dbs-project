var search_subcategory_id;

// set element visible
function show_element(element) {
  element.css('visibility', 'visible');
};

// set element hidden
function hide_element(element) {
  element.css('visibility', 'hidden');
};

// append product row to search result area
function append_product(product) {
  $product_row = $('<tr>');
  $product_row.append('<td class="col-md-1">' + (product.code || '') + '</td>');
  $product_row.append('<td class="col-md-3">' + (product.title || '') + '</td>');
  $product_row.append('<td class="col-md-1">' + (product.ean || '') + '</td>');
  $product_row.append('<td class="col-md-6">' + (product.description || '') + '</td>');
  $product_row.append($('<td class="col-md-1">').append(
    $('<a role="button">Add</a>').bind('click', function select_product() {

      if($('input[name="' + product.product_id + '"]').length) {
        // do not duplicate products in inquiry items
        alert('Product with this ID already in list.');
      }
      else {
        $inquiry_row = $('<tr>');
        $inquiry_row.append('<td class="col-md-2">' + (product.code || '') + '</td>');
        $inquiry_row.append('<td class="col-md-5">' + (product.title || '') + '</td>');
        $inquiry_row.append('<td class="col-md-2">' + (product.ean || '') + '</td>');
        $inquiry_row.append('<td class="col-md-2"><input name="' + (product.product_id || '') + '" value=1></td>');
        $inquiry_row.append($('<td class="col-md-1">').append(
          $('<a role="button">Delete</a>').bind('click', function delete_item() {
            // remove product from inquiry item list
            $(this).parent().parent().remove();

            if( $('#inquiry__table__body').children().length == 0 ) {
              // inquiry must contain at least 1 item when submitted
              hide_element($('#list__items'));
            }
        })));

        // add inquiry item tightened to selected product
        $('#inquiry__table__body').append($inquiry_row);
        show_element($('#list__items'));
      }
  })));

  $('#search__table__body').append($product_row);
};

// show info row instead of search results
function append_info(message) {
  $product_row = $('<tr>');
  $product_row.append('<td class="col-md-2">' + (message || '') + '</td>');
  $product_row.append('<td class="col-md-5">');
  $product_row.append('<td class="col-md-2">');
  $product_row.append('<td class="col-md-2">');
  $product_row.append('<td class="col-md-1">');

  $('#search__table__body').append($product_row);
};

// remove all rows from search result area
function remove_products() {
  $('#search__table__body').empty();
};

// load product with corresponding code asynchronously, then update table
function search_by_code(e) {
  remove_products();
  append_info('Loading...');

  code = $('input#input__code').val();
  if (!code) {
    return false;
  }

  $.getJSON($SCRIPT_ROOT + '/api/_search_by_code', {
    phrase_code: code
  }, function(data) {
    remove_products();

    product = data.result;
    if (product) {
      append_product(product);
    }
    else {
      append_info('Nothing found');
    }
  });
};

// load products with corresponding title match asynchronously, then update table
function search_by_title(e) {
  remove_products();
  append_info('Loading...');

  title = $('input#input__title').val();
  if (!title || !search_subcategory_id) {
    return false;
  }

  $.getJSON($SCRIPT_ROOT + '/api/_search_by_title', {
    phrase_title: title,
    subcategory_id: search_subcategory_id
  }, function(data) {
    remove_products();

    products = data.result;
    if (products.length) {
      for (i = 0; i < products.length; i++) {
        product = products[i];
        append_product(product);
      }
    }
    else {
      append_info('Nothing found');
    }
  });
};

// load subcategories for selected category asynchronously, then display drowpdown
function show_subcategories(category_id) {
  $('#subcategory__dropdown__menu').empty();

  $.getJSON($SCRIPT_ROOT + '/api/_subcategory_by_category', {
    category_id: category_id
  }, function(data) {
    subcategories = data.result;
    for (i = 0; i < subcategories.length; i++) {
      subcategory = subcategories[i];
      $('#subcategory__dropdown__menu').append(
        $('<button id="' + subcategory.subcategory_id + '"class="dropdown-item btn btn-secondary button__select__subcategory">' + subcategory.subcategory_name + '</button>').bind('click',select_subcategory));
    }
  });

  show_element($('#subcategory__dropdown'));
};

// user event select subcategory from category
function select_subcategory(e) {
  // remember subcategory to perform title search later
  search_subcategory_id = $(this).attr('id');
  $('#button__subcategory__dropdown').text($(this).text());
  show_element($('#button__search__title'));
};

// user event select category
function select_category(e) {
  category_id = $(this).attr('id');
  $('#button__category__dropdown').text($(this).text());
  show_subcategories(category_id);
};

$(function() {
  $('#button__search__code').bind('click', search_by_code);
  $('#button__search__title').bind('click', search_by_title);
  $('.button__select__category').bind('click', select_category);
});
