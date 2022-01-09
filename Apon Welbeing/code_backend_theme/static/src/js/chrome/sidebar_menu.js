odoo.define("code_backend_theme.SidebarMenu", function (require) {
  ("use strict");
  //sidebar toggle effect
  $(document).on("click", "#closeSidebar", function (event) {
    $("#closeSidebar").hide();
    $("#openSidebar").show();
  });
  $(document).on("click", "#openSidebar", function (event) {
    $("#openSidebar").hide();
    $("#closeSidebar").show();
    // if (window.matchMedia("(max-width: 990px)").matches) {
    //   $("#sidebar_panel").css({ display: "block !important" });
    //   alert("Okey");
    // } else {
    //   alert("not ok");
    // }
  });
  $(document).on("click", "#closeSidebar", function (event) {
    $("#sidebar_panel").css({ display: "block" });
    $(".o_action_manager").css({
      "margin-left": "200px",
      transition: "all .1s linear",
    });
    $(".top_heading").css({
      "margin-left": "200px",
      transition: "all .1s linear",
    });

    //add class in navbar
    var navbar = $(".o_main_navbar");
    var navbar_id = navbar.data("id");
    $("nav").addClass(navbar_id);
    navbar.addClass("small_nav");

    //add class in action-manager
    var action_manager = $(".o_action_manager");
    var action_manager_id = action_manager.data("id");
    $("div").addClass(action_manager_id);
    action_manager.addClass("sidebar_margin");

    //add class in top_heading
    var top_head = $(".top_heading");
    var top_head_id = top_head.data("id");
    $("div").addClass(top_head_id);
    top_head.addClass("sidebar_margin");
  });
  $(document).on("click", "#openSidebar", function (event) {
    $("#sidebar_panel").css({ display: "none" });
    $(".o_action_manager").css({ "margin-left": "0px" });
    $(".top_heading").css({ "margin-left": "0px" });

    //remove class in navbar
    var navbar = $(".o_main_navbar");
    var navbar_id = navbar.data("id");
    $("nav").removeClass(navbar_id);
    navbar.removeClass("small_nav");

    //remove class in action-manager
    var action_manager = $(".o_action_manager");
    var action_manager_id = action_manager.data("id");
    $("div").removeClass(action_manager_id);
    action_manager.removeClass("sidebar_margin");

    //remove class in top_heading
    var top_head = $(".top_heading");
    var top_head_id = top_head.data("id");
    $("div").removeClass(top_head_id);
    top_head.removeClass("sidebar_margin");
  });

  $(document).on("click", ".sidebar a", function (event) {
    var menu = $(".sidebar a");
    var $this = $(this);
    var id = $this.data("id");
    $("header").removeClass().addClass(id);
    menu.removeClass("active");
    $this.addClass("active");

    //sidebar close on menu-item click
    // $("#sidebar_panel").css({ display: "none" });
    // $(".o_action_manager").css({ "margin-left": "0px" });
    // $(".top_heading").css({ "margin-left": "0px" });
    // $("#closeSidebar").hide();
    // $("#openSidebar").show();

    //remove class in navbar
    var navbar = $(".o_main_navbar");
    var navbar_id = navbar.data("id");
    $("nav").removeClass(navbar_id);
    navbar.removeClass("small_nav");

    //remove class in action-manager
    var action_manager = $(".o_action_manager");
    var action_manager_id = action_manager.data("id");
    $("div").removeClass(action_manager_id);
    action_manager.removeClass("sidebar_margin");

    //remove class in top_heading
    var top_head = $(".top_heading");
    var top_head_id = top_head.data("id");
    $("div").removeClass(top_head_id);
    top_head.removeClass("sidebar_margin");
  });
  // Mobile side bar close
  $(document).on("click", "#openSidebar", function (event) {
    if (window.matchMedia("(max-width: 990px)").matches) {
      // $("#sidebar_panel").css({ display: "block" + "!important" });
      $("#sidebar_panel").attr("style", "display: block !important");
      // alert("Okey");
    }
  });
  $(document).on("click", "#closeSidebar", function (event) {
    if (window.matchMedia("(max-width: 990px)").matches) {
      // $("#sidebar_panel").css({ display: "block" + "!important" });
      $(".o_action_manager").attr("style", "margin-left:0 !important");
      $(".top_heading").attr("style", "margin-left:0 !important");
      // alert("Okey");
      $(document).on("click", ".sidebar a", function (event) {
        $("#sidebar_panel").css({ display: "none" });
        $(".o_action_manager").css({ "margin-left": "0px" });
        $(".top_heading").css({ "margin-left": "0px" });
        $("#closeSidebar").hide();
        $("#openSidebar").show();
      });
    }
  });

  // --------------------------------------------------------------
  function changeActivCclass() {
    // alert("The URL of this page is: " + window.location.href);
    let getUrl = window.location.href;
    console.log(getUrl, "Url Of This Page converted");

    var delayInMilliseconds = 2000; //1 second

    setTimeout(function () {
      // Get menu item Href
      let menuItem = document.querySelectorAll(".sidebar_menu .nav-link"); //Get meneu items
      let menuItemLength = menuItem.length; //get items length
      for (i = 0; i < menuItemLength; i++) {
        let itemLink = menuItem[i].href;
        let match = getUrl.match(itemLink);
        if (menuItem[i].href == match) {
          menuItem[i].classList.add("active");
        }
      }
    }, delayInMilliseconds);
  }
  changeActivCclass();
});
