(function(){

    var recipePrefix = '/api/v1/recipe/';

    angular.module('recipehub')
        .service('RecipeService', ['$http', function recipeService($http) {
            this.getTopFive = function () {
                return $http.get(recipePrefix, {
                    params: {
                        top_five: 1
                    }
                });
            };
        }]);
})();
