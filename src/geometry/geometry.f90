module geometry
    use precision, only: wp
    use asserts, only: assert
    use maths_utils, only: norm

    private

    !> Type Atom
    type atom_type
        !> Position in angstrom
        real(wp), dimension(3) :: position
        !> Species label
        character(len=3) :: symbol
        !> Atomic number
        integer :: an
    end type atom_type


    interface distance_matrix
        module procedure distance_matrix_from_positions, distance_matrix_from_molecule
    end interface distance_matrix


    public :: distance_matrix, atom_type


contains

    !TODO(Alex) Code up some test systems (crystals)

    !> @brief Construct distance matrix
    !>
    !> Given a set of atomic positions, construct a distance matrix
    !>
    !> @param positions atomic positions
    !> @parm d distance matrix
    function distance_matrix_from_positions(positions) result(d)
        real(wp), intent(in) :: positions(:,:)
        real(wp), allocatable :: d(:,:)
        integer :: ia, ja, n_atoms

        call assert(size(positions, 1) == 3, &
                message = "Distance matrix expects atomic coordinates stored (3, n_atoms)")

        n_atoms = size(positions, 2)
        allocate(d(n_atoms, n_atoms))

        do ia = 1, n_atoms
            do ja = ia, n_atoms
                d(ia, ja) = norm(positions(ja, :) - positions(ia, :))
                d(ja, ia) = d(ia, ja)
            enddo
        enddo

    end function distance_matrix_from_positions

    !> @brief Construct distance matrix
    !>
    !> Given an array of atoms type, construct a distance matrix
    !>
    !> @param[in] molecule   array of atoms with type \p atom_type
    !> @param[out] d  distance matrix
    function distance_matrix_from_molecule(molecule) result(d)
        type(atom_type), intent(in) :: molecule(:)
        real(wp), allocatable :: d(:,:)
        integer :: ia, ja, n_atoms
        real(wp) :: r_a(3)

        n_atoms = size(molecule)
        allocate(d(n_atoms, n_atoms))

        do ia = 1, n_atoms
            r_a = molecule(ia)%position
            do ja = ia, n_atoms
                d(ia, ja) = norm(molecule(ib)%position - r_a)
                d(ja, ia) = d(ia, ja)
            enddo
        enddo

    end function distance_matrix_from_molecule

end module geometry