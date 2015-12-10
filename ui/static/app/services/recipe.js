(function(){

    var prefix = '/api/v1/recipe/';
    var forkPrefix = '/api/v1/fork/';
    var versionPrefix = '/api/v1/version/';

    angular.module('recipehub')
        .service('RecipeService', ['$http', function recipeService($http) {
            this.getTopFive = function () {
                return $http.get(prefix, {
                    params: {
                        top_five: 1
                    }
                });
            };

            this.getUserRecipes = function (userId) {
                return $http.get(prefix, {
                    params: {
                        user_id: userId
                    }
                });
            };

            this.getRecipe = function (id, version_id) {
                return $http.get(prefix + id + '/', {
                    params: {
                        version_id: version_id
                    }
                });
            };

            this.forkRecipe = function (id) {
                return $http.post(forkPrefix, JSON.stringify({
                    recipe_id: id
                }));
            };

            this.newRecipe = function (recipe) {
                return $http.post(prefix, JSON.stringify(recipe));
            };

            this.updateRecipe = function (id, recipe) {
                return $http.put(prefix + id + '/', JSON.stringify(recipe));
            };


            this.getForks = function (id) {
                return $http({
                    url: forkPrefix,
                    method: "GET",
                    params: {recipe_id: id}
                });
            };

            this.getVersions = function (id) {
                return $http({
                    url: versionPrefix + id + '/',
                    method: "GET"
                });
            };

        }]);
})();
