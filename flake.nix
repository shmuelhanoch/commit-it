{
  description = "Local LLM Git commit message generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        isDarwin = pkgs.stdenv.isDarwin;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python314
            uv
            git
          ] ++ (lib.optionals (!isDarwin) [ ollama ]);

          shellHook = ''
            if [ ! -d ".venv" ]; then
              uv venv .venv --python 3.14
            fi
            source .venv/bin/activate
            uv pip install -e . --quiet
          '';
        };
      });
}
