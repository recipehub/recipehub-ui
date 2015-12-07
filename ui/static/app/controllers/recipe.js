(function(){
    angular.module('recipehub')
        .controller('RecipeController', ['RecipeService', function recipeController($recipeService) {
            $recipeService.getTopFive()
                .then(function(data) {
                });
        }]);
})();
