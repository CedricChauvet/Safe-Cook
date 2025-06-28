// This is a shim for web and Android where the tab bar is generally opaque.
export default undefined;
export { default } from './TabBarBackground.ios';

export function useBottomTabOverflow() {
  return 0;
}
