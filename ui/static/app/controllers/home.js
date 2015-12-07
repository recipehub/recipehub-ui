(function(){
    angular.module('recipehub')
        .controller('HomeController', ['RecipeService', '$scope', function HomeController($recipeService, $scope) {
            var self = this;

            $recipeService.getTopFive()
                .then(function(response) {
                    $scope.recipes = response.data;
                });
        }]);

})();
