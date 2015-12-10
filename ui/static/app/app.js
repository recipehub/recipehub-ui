(function(){
    'use strict';

    angular
        .module('recipehub', ['ngMaterial', 'ngRoute', 'angular-sortable-view', 'ui.gravatar', 'ngCookies', 'angular-input-stars'])
        .config(function($mdIconProvider, $mdThemingProvider, $routeProvider) {

            $mdIconProvider
                .defaultIconSet("./assets/svg/avatars.svg", 128)
                .icon("menu"       , "./assets/svg/menu.svg"        , 24)
                .icon("share"      , "./assets/svg/share.svg"       , 24)
                .icon("google_plus", "./assets/svg/google_plus.svg" , 512)
                .icon("hangouts"   , "./assets/svg/hangouts.svg"    , 512)
                .icon("twitter"    , "./assets/svg/twitter.svg"     , 512)
                .icon("phone"      , "./assets/svg/phone.svg"       , 512);

            $mdThemingProvider.theme('default')
                .primaryPalette('brown')
                .accentPalette('red');

            $routeProvider.
                when('/', {
                    templateUrl: '/static/app/templates/home.html',
                    controller: 'HomeController'
                }).
                when('/search', {
                    templateUrl: '/static/app/templates/home.html',
                    controller: 'SearchController'
                }).
                when('/myrecipes', {
                    templateUrl: '/static/app/templates/home.html',
                    controller: 'MyRecipesController'
                }).
                when('/recipe/new', {
                    templateUrl: '/static/app/templates/includes/recipe-new.html',
                    controller: 'NewRecipeController'
                }).
                when('/recipe/edit/:id', {
                    templateUrl: '/static/app/templates/includes/recipe-edit.html',
                    controller: 'EditRecipeController'
                }).
                when('/recipe/:id', {
                    templateUrl: '/static/app/templates/recipe.html',
                    controller: 'RecipeController'
                });
        })
        .
        run([
            '$http', 
            '$cookies', 
            function($http, $cookies) {
                $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
                $http.defaults.headers.put['X-CSRFToken'] = $cookies.get('csrftoken');
                $http.defaults.headers.put['Content-Type'] = 'application/json'
            }]);

})();
