{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  languages.python = {
    enable = true;
  };

  packages = with pkgs.python313Packages; [
    seaborn
    matplotlib
    pandas
    termcolor
    rich
  ];

}
