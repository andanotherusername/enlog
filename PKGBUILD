pkgname=enlog
pkgdesc="Gathers selected system logs and generates a sharable link."
url="https://github.com/andanotherusername/enlog.git"
pkgver=0.1
pkgrel=1

arch=("any")
license=("GPL")
depends=(python-pycurl python-pyperclip python-pyqt5)

source=(
    enlog/main.py
    enui/EnUI.py
    setup.py
)

sha512sums=(
    '8510002470cd22056a8311763566efcbc0c219410fc5387eb7cb91fdd2b3be62e2a919cbc3bfd09b65f56167091876cfb09e775ca5d8cbbe8513fca84f84001f'
    'cf404a9c1740c5d5af2c68f039ea6d99c264dd9c0e73747c356c71027f502f4daa03badc0d2c2c15658a36920575903dcea7ad7e90a12157aacd49ca5c757a1f'
    '19fd1f732b1d452d53ee1eb3ead3545d12a1f896c6908fac774d8bf373b6c6bbd33261f28cdb8393d5cec31cd3bdd45a52807f2b88c4ff63101e97f8c3aee60a'
)

package(){
    python setup.py install --home=$pkgdir \
                            --install-scripts=$pkgdir/usr/bin/
    install -d $pkgdir/usr/share/applications
    install -Dm755 $pkgname.desktop         $pkgdir/usr/share/applications/$pkgname.desktop
}
