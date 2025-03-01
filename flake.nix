{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { nixpkgs, ... }@inputs: {

    devShells = builtins.listToAttrs (map (system: {
        name = system;
        value = with import nixpkgs { inherit system; config.allowUnfree = true; }; rec {

          esp32-dev = pkgs.mkShell {
            packages = with pkgs; [
              micropython
              esptool
              adafruit-ampy
              picocom
            ] ++ (with python3Packages; [
              pip
              numpy
              python-lsp-server
            ]) ++ [
              (writeShellScriptBin ''mp-erase'' ''esptool.py --port /dev/ttyUSB0 erase_flash'')
              (writeShellScriptBin ''mp-deploy-firmware'' ''esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash 0x1000'')
              (writeShellScriptBin ''mp-REPL'' ''picocom /dev/ttyUSB0 -b115200'')
              (writeShellScriptBin ''mp-flash'' ''ampy --port /dev/ttyUSB0 put'')
            ];

            PIP_PREFIX = ''_pip_packages'';
            PYTHONPATH = ''$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH'';
            PATH = ''$PIP_PREFIX/bin:$PATH'';

            shellHook = ''
              unset SOURCE_DATE_EPOCH
              if [ ! -d "$PIP_PREFIX" ]; then
               pip install micropython-esp32-stubs
               pip install micropython-esp32-stubs
              fi
            '';
          };

          default = esp32-dev;
        };
    })[ "x86_64-linux" ]);
  };
}
