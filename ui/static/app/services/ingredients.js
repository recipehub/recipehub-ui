(function(){

    var prefix = '/api/v1/ingredient/';

    angular.module('recipehub')
        .service('IngredientService', ['$http', function recipeService($http) {
            this.getIngredients = function () {
                return $http.get(prefix);
            };
        }]);
})();
